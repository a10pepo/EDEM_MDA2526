import os
import boto3
from botocore.exceptions import ClientError


def get_dynamodb_resource():
    if os.getenv("USE_LOCAL_DYNAMODB", "false").lower() == "true":
        endpoint = os.getenv("DYNAMODB_ENDPOINT", "http://localhost:4566")
        return boto3.resource(
            "dynamodb",
            endpoint_url=endpoint,
            region_name="us-east-1",
            aws_access_key_id="local",
            aws_secret_access_key="local",
        )
    return boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION", "us-east-1"))


def get_table(table_name: str):
    return get_dynamodb_resource().Table(table_name)


PRODUCTS_TABLE = os.getenv("PRODUCTS_TABLE", "zara_products")
TICKETS_TABLE = os.getenv("TICKETS_TABLE", "zara_tickets")
CUSTOMERS_TABLE = os.getenv("CUSTOMERS_TABLE", "zara_customers")


def create_tables():
    dynamodb = get_dynamodb_resource()
    tables = [
        {
            "TableName": PRODUCTS_TABLE,
            "KeySchema": [{"AttributeName": "sku", "KeyType": "HASH"}],
            "AttributeDefinitions": [{"AttributeName": "sku", "AttributeType": "S"}],
            "BillingMode": "PAY_PER_REQUEST",
        },
        {
            "TableName": TICKETS_TABLE,
            "KeySchema": [{"AttributeName": "ticket_id", "KeyType": "HASH"}],
            "AttributeDefinitions": [{"AttributeName": "ticket_id", "AttributeType": "S"}],
            "BillingMode": "PAY_PER_REQUEST",
        },
        {
            "TableName": CUSTOMERS_TABLE,
            "KeySchema": [{"AttributeName": "customer_id", "KeyType": "HASH"}],
            "AttributeDefinitions": [{"AttributeName": "customer_id", "AttributeType": "S"}],
            "BillingMode": "PAY_PER_REQUEST",
        },
    ]
    created = []
    for table_def in tables:
        name = table_def["TableName"]
        try:
            dynamodb.create_table(**table_def)
            created.append(name)
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceInUseException":
                pass  # table already exists
            else:
                raise
    return created
