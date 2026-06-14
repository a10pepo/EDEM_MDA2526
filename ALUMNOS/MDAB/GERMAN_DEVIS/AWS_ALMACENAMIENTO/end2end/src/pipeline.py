"""
pipeline.py — Full F1 data pipeline in one command.

  1. Inserts/updates data in RDS (idempotent, ON CONFLICT DO NOTHING)
  2. Syncs RDS → Parquet on S3 → Glue Catalog (full-refresh)

Prerequisites:
  - db/init.sql has been run against RDS to create the tables
  - .env is configured with both RDS and AWS credentials

Run:
  python src/pipeline.py

To add new races tomorrow:
  1. Append new race dict to `races` in src/initial_info.py
  2. python src/pipeline.py  (only new rows go to RDS; Glue gets full-refresh)
"""

from load_rds import main as load_rds
from load_glue import main as load_glue

if __name__ == "__main__":
    print("=== Step 1: RDS load ===")
    load_rds()
    print("\n=== Step 2: Glue sync (RDS → Parquet) ===")
    load_glue()
    print("\nDone.")
