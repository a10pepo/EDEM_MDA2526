"""
load_lake.py — Sync Zara data from DynamoDB → Parquet files on S3 → Glue Catalog.

Flow:
  DynamoDB (source of truth) → Parquet files on S3 → Glue external tables → Athena

Run standalone:
  python aws/load_lake.py
"""
import sys
import os
import io

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import boto3
import pandas as pd
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

from src.services.product_service import list_products
from src.services.ticket_service import list_tickets
from src.services.customer_service import list_customers

AWS_REGION = os.environ["AWS_REGION"]
S3_BUCKET = os.environ["S3_BUCKET"]
GLUE_DATABASE = os.environ["GLUE_DATABASE"]

s3 = boto3.client("s3", region_name=AWS_REGION)
glue = boto3.client("glue", region_name=AWS_REGION)


def products_to_records():
    return [p.to_dynamodb_item() | {"price": p.price} for p in list_products()]


def customers_to_records():
    return [c.to_dynamodb_item() for c in list_customers()]


def tickets_to_records():
    return [
        {
            "ticket_id": t.ticket_id,
            "cashier_id": t.cashier_id,
            "date_time": t.date_time,
            "payment_method": t.payment_method,
            "status": t.status,
            "customer_id": t.customer_id,
            "total_amount": t.total_amount(),
            "discount_percentage": t.discount_percentage(),
        }
        for t in list_tickets()
    ]


def ticket_items_to_records():
    records = []
    for t in list_tickets():
        for item in t.items:
            records.append({
                "ticket_id": t.ticket_id,
                "sku": item.sku,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "discount": item.discount,
                "subtotal": item.subtotal(),
            })
    return records


def col(name, t):
    return {"Name": name, "Type": t}


GLUE_SCHEMAS = {
    "products": [
        col("sku", "string"), col("name", "string"), col("category", "string"),
        col("size", "string"), col("color", "string"), col("price", "double"),
        col("stock_quantity", "int"), col("restock_threshold", "int"),
        col("last_restock_date", "string"), col("supplier_id", "string"),
    ],
    "customers": [
        col("customer_id", "string"), col("name", "string"), col("email", "string"),
        col("phone", "string"), col("date_of_birth", "string"), col("membership_level", "string"),
    ],
    "tickets": [
        col("ticket_id", "string"), col("cashier_id", "string"), col("date_time", "string"),
        col("payment_method", "string"), col("status", "string"), col("customer_id", "string"),
        col("total_amount", "double"), col("discount_percentage", "double"),
    ],
    "ticket_items": [
        col("ticket_id", "string"), col("sku", "string"), col("quantity", "int"),
        col("unit_price", "double"), col("discount", "double"), col("subtotal", "double"),
    ],
}

RECORD_BUILDERS = {
    "products": products_to_records,
    "customers": customers_to_records,
    "tickets": tickets_to_records,
    "ticket_items": ticket_items_to_records,
}


def df_to_parquet_bytes(records):
    buf = io.BytesIO()
    pd.DataFrame(records).to_parquet(buf, index=False, engine="pyarrow")
    return buf.getvalue()


def upload(key, data):
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=data)


def register_glue_table(name, s3_prefix, columns):
    storage = {
        "Location": f"s3://{S3_BUCKET}/{s3_prefix}",
        "InputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
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
            create_kwargs = {"Bucket": S3_BUCKET}
            if AWS_REGION != "us-east-1":
                create_kwargs["CreateBucketConfiguration"] = {"LocationConstraint": AWS_REGION}
            s3.create_bucket(**create_kwargs)
            print(f"  Created bucket: {S3_BUCKET}")
        else:
            raise


def ensure_database():
    try:
        glue.create_database(DatabaseInput={"Name": GLUE_DATABASE})
        print(f"  Created Glue database: {GLUE_DATABASE}")
    except ClientError as e:
        if e.response["Error"]["Code"] != "AlreadyExistsException":
            raise


def main():
    ensure_bucket()
    ensure_database()

    for name, build_records in RECORD_BUILDERS.items():
        records = build_records()
        data = df_to_parquet_bytes(records)
        key = f"zara/{name}/data.parquet"
        upload(key, data)
        action = register_glue_table(name, f"zara/{name}/", GLUE_SCHEMAS[name])
        print(f"  {name}: uploaded {len(records)} rows -> s3://{S3_BUCKET}/{key} | Glue: {action}")

    print(f"\nGlue sync complete. Query with Athena: SELECT * FROM \"{GLUE_DATABASE}\".products LIMIT 10;")


if __name__ == "__main__":
    main()
