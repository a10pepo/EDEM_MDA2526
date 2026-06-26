"""
Run this script once to create the DynamoDB tables.
  Local:  USE_LOCAL_DYNAMODB=true python aws/setup_tables.py
  AWS:    python aws/setup_tables.py   (uses IAM role / env credentials)
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

from src.db.dynamodb import create_tables, PRODUCTS_TABLE, TICKETS_TABLE, CUSTOMERS_TABLE

if __name__ == "__main__":
    print(f"Target tables: {PRODUCTS_TABLE}, {TICKETS_TABLE}, {CUSTOMERS_TABLE}")
    created = create_tables()
    if created:
        for name in created:
            print(f"  Created: {name}")
    else:
        print("  All tables already exist.")
    print("Done.")
