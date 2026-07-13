import os
import pytest
import boto3
from moto import mock_aws


@pytest.fixture(autouse=True)
def aws_env(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.setenv("USE_LOCAL_DYNAMODB", "false")
    monkeypatch.setenv("PRODUCTS_TABLE", "zara_products")
    monkeypatch.setenv("TICKETS_TABLE", "zara_tickets")
    monkeypatch.setenv("CUSTOMERS_TABLE", "zara_customers")


@pytest.fixture
def dynamodb_tables(aws_env):
    with mock_aws():
        db = boto3.resource("dynamodb", region_name="us-east-1")
        db.create_table(
            TableName="zara_products",
            KeySchema=[{"AttributeName": "sku", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "sku", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        db.create_table(
            TableName="zara_tickets",
            KeySchema=[{"AttributeName": "ticket_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "ticket_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        db.create_table(
            TableName="zara_customers",
            KeySchema=[{"AttributeName": "customer_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "customer_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        yield db
