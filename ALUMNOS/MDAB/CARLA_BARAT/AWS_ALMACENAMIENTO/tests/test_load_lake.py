import io
import os

os.environ.setdefault("AWS_REGION", "us-east-1")
os.environ.setdefault("S3_BUCKET", "zara-test-bucket")
os.environ.setdefault("GLUE_DATABASE", "zara_test_db")

import boto3
import pandas as pd
import pytest
from moto import mock_aws

from aws import load_lake
from src.models.product import Product
from src.models.customer import Customer
from src.models.ticket import Ticket, TicketItem
from src.services.product_service import register_product
from src.services.customer_service import register_customer
from src.services.ticket_service import register_ticket


def make_product(sku="SKU-001") -> Product:
    return Product(
        sku=sku, name="Test Shirt", category="shirt", size="M",
        color="White", price=29.95, stock_quantity=20,
        restock_threshold=10, last_restock_date="2026-05-01",
        supplier_id="SUP-001",
    )


def make_customer(customer_id="DNI-001") -> Customer:
    return Customer(
        customer_id=customer_id, name="Test User",
        email="test@test.com", phone="600000000",
        date_of_birth="1990-01-01", membership_level="basic",
    )


def make_ticket(ticket_id="TKT-001") -> Ticket:
    return Ticket(
        ticket_id=ticket_id, cashier_id="C01",
        date_time="2026-06-01T10:00:00", payment_method="card",
        status="completed", customer_id="DNI-001",
        items=[TicketItem(sku="SKU-001", quantity=2, unit_price=29.95, discount=0.0)],
    )


def test_df_to_parquet_bytes_roundtrip():
    records = [{"sku": "SKU-001", "price": 29.95}]
    data = load_lake.df_to_parquet_bytes(records)
    df = pd.read_parquet(io.BytesIO(data))
    assert df.to_dict("records") == records


def test_ensure_bucket_creates_and_is_idempotent(aws_env):
    with mock_aws():
        load_lake.ensure_bucket()
        load_lake.ensure_bucket()  # no debe fallar si ya existe
        load_lake.s3.head_bucket(Bucket=load_lake.S3_BUCKET)


def test_ensure_database_creates_and_is_idempotent(aws_env):
    with mock_aws():
        load_lake.ensure_database()
        load_lake.ensure_database()  # no debe fallar si ya existe
        load_lake.glue.get_database(Name=load_lake.GLUE_DATABASE)


def test_register_glue_table_create_then_update(aws_env):
    with mock_aws():
        load_lake.ensure_database()
        columns = [{"Name": "sku", "Type": "string"}]
        assert load_lake.register_glue_table("products", "zara/products/", columns) == "created"
        assert load_lake.register_glue_table("products", "zara/products/", columns) == "updated"


def test_main_syncs_dynamodb_to_s3_and_glue(dynamodb_tables, monkeypatch):
    monkeypatch.setenv("PRODUCTS_TABLE", "zara_products")
    monkeypatch.setenv("TICKETS_TABLE", "zara_tickets")
    monkeypatch.setenv("CUSTOMERS_TABLE", "zara_customers")

    register_product(make_product())
    register_customer(make_customer())
    register_ticket(make_ticket())

    load_lake.main()

    s3 = boto3.client("s3", region_name="us-east-1")
    glue = boto3.client("glue", region_name="us-east-1")

    for name in ("products", "customers", "tickets", "ticket_items"):
        obj = s3.get_object(Bucket=load_lake.S3_BUCKET, Key=f"zara/{name}/data.parquet")
        df = pd.read_parquet(io.BytesIO(obj["Body"].read()))
        assert len(df) == 1
        glue.get_table(DatabaseName=load_lake.GLUE_DATABASE, Name=name)
