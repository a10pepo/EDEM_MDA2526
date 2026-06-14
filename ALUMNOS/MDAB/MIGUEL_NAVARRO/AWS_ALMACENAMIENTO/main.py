import pandas as pd

from config import CSV_PATH, load_lakehouse_config, load_rds_config, load_redshift_config
from database import (
    create_redshift_tables,
    create_rds_tables,
    get_rds_connection,
    get_redshift_connection,
)
from lakehouse_pipeline import run_lakehouse_el
from pipeline import clean_dataframe, load_data
from redshift_pipeline import run_el


def run_pipeline() -> None:
    print("Reading Hevy CSV...")
    df = clean_dataframe(pd.read_csv(CSV_PATH))
    print(f"  {len(df)} rows loaded.")

    print("Connecting to the database...")
    config = load_rds_config()
    conn = get_rds_connection(config)

    try:
        print("Creating tables (if they do not exist)...")
        create_rds_tables(conn)

        load_data(df, conn)

        print("Data successfully uploaded to AWS RDS!")

    except Exception as e:
        print(f"Error during ingestion: {e}")
        raise

    finally:
        conn.close()
        print("Database connection closed.")


def run_el_step() -> None:
    print("Connecting to RDS and Redshift for the EL step...")
    rds_conn = get_rds_connection(load_rds_config())
    redshift_conn = get_redshift_connection(load_redshift_config())

    try:
        print("Creating Redshift analytical tables (if they do not exist)...")
        create_redshift_tables(redshift_conn)

        run_el(rds_conn, redshift_conn)

        print("Data successfully replicated from RDS to Redshift!")

    except Exception as e:
        print(f"Error during RDS-to-Redshift EL: {e}")
        raise

    finally:
        rds_conn.close()
        redshift_conn.close()
        print("RDS and Redshift connections closed.")


def run_lakehouse_step() -> None:
    print("Connecting to RDS for the Lakehouse EL step...")
    rds_conn = get_rds_connection(load_rds_config())
    config = load_lakehouse_config()

    try:
        print(f"Target Iceberg lakehouse -> s3://{config.s3_bucket} / glue database '{config.glue_database}'")

        run_lakehouse_el(rds_conn, config)

        print("Data successfully written to the S3/Glue Iceberg lakehouse!")

    except Exception as e:
        print(f"Error during RDS-to-Lakehouse EL: {e}")
        raise

    finally:
        rds_conn.close()
        print("RDS connection closed.")


if __name__ == "__main__":
    run_pipeline()
    run_el_step()
    run_lakehouse_step()
