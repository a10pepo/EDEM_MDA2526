"""
pipeline.py — Full Zara data pipeline in one command.

  1. Creates DynamoDB tables and seeds demo data (operational layer)
  2. Syncs DynamoDB → Parquet on S3 → Glue Catalog (data lake, full-refresh)

Prerequisites:
  - .env is configured with DynamoDB and AWS (S3/Glue) settings

Run:
  python aws/pipeline.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

if __name__ == "__main__":
    print("=== Step 1: DynamoDB setup + seed ===")
    from seed_data import PRODUCTS, CUSTOMERS, TICKETS
    from src.db.dynamodb import create_tables
    from src.services.product_service import register_product
    from src.services.customer_service import register_customer
    from src.services.ticket_service import register_ticket

    create_tables()
    for p in PRODUCTS:
        register_product(p)
    for c in CUSTOMERS:
        register_customer(c)
    for t in TICKETS:
        register_ticket(t)

    print("\n=== Step 2: Glue sync (DynamoDB -> Parquet -> Glue) ===")
    from load_lake import main as load_lake
    load_lake()

    print("\nDone.")
