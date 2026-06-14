import awswrangler as wr
import pandas as pd
from psycopg2.extensions import connection as Connection

from config import LakehouseConfig

# =============================================================================
# Extract — pull a denormalised view of the OLTP schema from RDS
# =============================================================================

EXTRACT_QUERY = """
SELECT
    s.set_id,
    w.workout_id,
    w.title          AS workout_title,
    w.start_time,
    w.end_time,
    e.exercise_id,
    e.exercise_title,
    s.superset_id,
    s.set_index,
    s.set_type,
    s.weight_kg,
    s.reps,
    s.distance_km,
    s.duration_seconds,
    s.rpe
FROM sets s
JOIN workouts w  ON w.workout_id = s.workout_id
JOIN exercises e ON e.exercise_id = s.exercise_id;
"""

ICEBERG_TABLE = "fact_sets"


def extract_from_rds(rds_conn: Connection) -> pd.DataFrame:
    """Read the joined workouts/exercises/sets data from RDS into a DataFrame."""
    return pd.read_sql(EXTRACT_QUERY, rds_conn)


# =============================================================================
# Load — write the extracted rows into the S3/Glue Iceberg lakehouse table
# =============================================================================

def load_to_iceberg(df: pd.DataFrame, config: LakehouseConfig) -> None:
    """Write the given DataFrame to S3 in Iceberg format and register it in AWS Glue."""
    temp_path=  f"s3://{config.s3_bucket}/tmp/{ICEBERG_TABLE}/"
    table_location = f"s3://{config.s3_bucket}/lakehouse/{ICEBERG_TABLE}/"
    s3_output = f"s3://{config.s3_bucket}/athena_output/"

    wr.athena.to_iceberg(
        df=df,
        dtype={"rpe": "int"},
        database=config.glue_database,
        table=ICEBERG_TABLE,
        temp_path=temp_path,
        table_location=table_location,
        s3_output=s3_output,
        mode="overwrite",
        keep_files=False,
    )
    print(f"  Rows written to Iceberg table '{config.glue_database}.{ICEBERG_TABLE}': {len(df)}")


def run_lakehouse_el(rds_conn: Connection, config: LakehouseConfig) -> None:
    """Extract from RDS and load into the S3/Glue Iceberg lakehouse, end to end."""
    print("Extracting data from RDS...")
    df = extract_from_rds(rds_conn)
    print(f"  {len(df)} rows extracted.")

    print("Writing data to S3 as Iceberg and registering it in AWS Glue...")
    load_to_iceberg(df, config)
