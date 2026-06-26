from typing import List, Optional
from botocore.exceptions import ClientError
from src.db.dynamodb import get_table, PRODUCTS_TABLE
from src.models.product import Product


def register_product(product: Product) -> bool:
    try:
        get_table(PRODUCTS_TABLE).put_item(Item=product.to_dynamodb_item())
        return True
    except ClientError:
        return False


def get_product(sku: str) -> Optional[Product]:
    response = get_table(PRODUCTS_TABLE).get_item(Key={"sku": sku})
    item = response.get("Item")
    return Product.from_dynamodb_item(item) if item else None


def list_products() -> List[Product]:
    response = get_table(PRODUCTS_TABLE).scan()
    return [Product.from_dynamodb_item(i) for i in response.get("Items", [])]


def update_stock(sku: str, new_quantity: int) -> bool:
    try:
        get_table(PRODUCTS_TABLE).update_item(
            Key={"sku": sku},
            UpdateExpression="SET stock_quantity = :q",
            ExpressionAttributeValues={":q": new_quantity},
        )
        return True
    except ClientError:
        return False


def delete_product(sku: str) -> bool:
    try:
        get_table(PRODUCTS_TABLE).delete_item(Key={"sku": sku})
        return True
    except ClientError:
        return False
