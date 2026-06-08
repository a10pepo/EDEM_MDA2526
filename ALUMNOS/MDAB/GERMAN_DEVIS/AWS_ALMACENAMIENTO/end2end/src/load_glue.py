"""
load_glue.py — Sync F1 data from RDS → Parquet files on S3 → Glue Catalog.

Flow:
  RDS (source of truth) → Parquet files on S3 → Glue external tables → Athena

This script reads current data from RDS and does a full-refresh of the
Glue/S3 layer. Run it after load_rds.py (or use pipeline.py to do both).

Add to .env:
  AWS_REGION=eu-north-1
  S3_BUCKET=f1-datalake-edem2526
  GLUE_DATABASE=db 1
  PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE

Run standalone:
  python src/load_glue.py
"""

import io
import os
import sys
import boto3
import pandas as pd
import psycopg2
import psycopg2.extras
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

AWS_REGION    = os.environ["AWS_REGION"]
S3_BUCKET     = os.environ["S3_BUCKET"]
GLUE_DATABASE = os.environ["GLUE_DATABASE"]

s3   = boto3.client("s3",   region_name=AWS_REGION)
glue = boto3.client("glue", region_name=AWS_REGION)


def get_rds_connection():
    return psycopg2.connect(
        host=os.environ["PGHOST"],
        port=os.environ.get("PGPORT", 5432),
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        dbname=os.environ["PGDATABASE"],
    )


def fetch_table(conn, table):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(f"SELECT * FROM {table}")
        return [dict(r) for r in cur.fetchall()]


def df_to_parquet_bytes(records):
    buf = io.BytesIO()
    pd.DataFrame(records).to_parquet(buf, index=False, engine="pyarrow")
    return buf.getvalue()


def upload(key, data):
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=data)


def col(name, t):
    return {"Name": name, "Type": t}


GLUE_SCHEMAS = {
    "teams": [
        col("team_id", "string"), col("name", "string"), col("base", "string"),
        col("team_principal", "string"), col("power_unit", "string"),
        col("founded_year", "int"), col("championships", "int"),
    ],
    "drivers": [
        col("driver_id", "string"), col("team_id", "string"), col("code", "string"),
        col("name", "string"), col("nationality", "string"),
        col("date_of_birth", "string"), col("permanent_number", "int"),
    ],
    "races": [
        col("race_id", "string"), col("name", "string"), col("circuit", "string"),
        col("country", "string"), col("date", "string"), col("season", "int"),
        col("round", "int"), col("laps", "int"),
    ],
    "results": [
        col("race_id", "string"), col("driver_id", "string"),
        col("grid_position", "int"), col("final_position", "int"),
        col("points", "double"), col("status", "string"),
    ],
}


def register_glue_table(name, s3_prefix, columns):
    storage = {
        "Location": f"s3://{S3_BUCKET}/{s3_prefix}",
        "InputFormat":  "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
        "OutputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
        "SerdeInfo": {
            "SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe",
        },
        "Columns": columns,
    }
    table_input = {
        "Name": name,
        "StorageDescriptor": storage,
        "TableType": "EXTERNAL_TABLE",
        "Parameters": {"classification": "parquet"},
    }
    try:
        glue.create_table(DatabaseName=GLUE_DATABASE, TableInput=table_input)
        return "created"
    except ClientError as e:
        if e.response["Error"]["Code"] == "AlreadyExistsException":
            glue.update_table(DatabaseName=GLUE_DATABASE, TableInput=table_input)
            return "updated"
        raise


def ensure_bucket():
    try:
        s3.head_bucket(Bucket=S3_BUCKET)
    except ClientError as e:
        if e.response["Error"]["Code"] in ("404", "NoSuchBucket"):
            s3.create_bucket(
                Bucket=S3_BUCKET,
                CreateBucketConfiguration={"LocationConstraint": AWS_REGION},
            )
            print(f"  Created bucket: {S3_BUCKET}")
        else:
            raise


def main():
    ensure_bucket()

    try:
        conn = get_rds_connection()
    except KeyError as e:
        print(f"Missing environment variable: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        tables = {name: fetch_table(conn, name) for name in GLUE_SCHEMAS}
    finally:
        conn.close()

    for name, records in tables.items():
        data = df_to_parquet_bytes(records)
        key = f"f1/{name}/data.parquet"
        upload(key, data)
        action = register_glue_table(name, f"f1/{name}/", GLUE_SCHEMAS[name])
        print(f"  {name}: uploaded {len(records)} rows → s3://{S3_BUCKET}/{key} | Glue: {action}")

    print(f"\nGlue sync complete. Query with Athena: SELECT * FROM \"{GLUE_DATABASE}\".teams LIMIT 10;")


if __name__ == "__main__":
    main()
