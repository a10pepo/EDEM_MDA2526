from typing import List, Optional
from botocore.exceptions import ClientError
from src.db.dynamodb import get_table, CUSTOMERS_TABLE
from src.models.customer import Customer


def register_customer(customer: Customer) -> bool:
    try:
        get_table(CUSTOMERS_TABLE).put_item(Item=customer.to_dynamodb_item())
        return True
    except ClientError:
        return False


def get_customer(customer_id: str) -> Optional[Customer]:
    response = get_table(CUSTOMERS_TABLE).get_item(Key={"customer_id": customer_id})
    item = response.get("Item")
    return Customer.from_dynamodb_item(item) if item else None


def list_customers() -> List[Customer]:
    response = get_table(CUSTOMERS_TABLE).scan()
    return [Customer.from_dynamodb_item(i) for i in response.get("Items", [])]


def delete_customer(customer_id: str) -> bool:
    try:
        get_table(CUSTOMERS_TABLE).delete_item(Key={"customer_id": customer_id})
        return True
    except ClientError:
        return False
