"""
Borra todos los datos de DynamoDB y los ficheros Parquet de S3.
Usar antes de una recarga completa del pipeline.

Uso: python scripts/reset_data.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import boto3
from src import config

_dynamodb = boto3.resource("dynamodb", region_name=config.AWS_REGION)
_s3       = boto3.client("s3",         region_name=config.AWS_REGION)


def clear_dynamo_table(table_name: str, pk_field: str) -> int:
    """
    Borra todos los items de una tabla DynamoDB.
    Usa ExpressionAttributeNames para manejar campos con nombre reservado (ej: "date").
    """
    table = _dynamodb.Table(table_name)
    scan_kwargs = {
        "ProjectionExpression":    "#pk",
        "ExpressionAttributeNames": {"#pk": pk_field},
    }
    response = table.scan(**scan_kwargs)
    items    = response["Items"]
    while "LastEvaluatedKey" in response:
        response = table.scan(**scan_kwargs, ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response["Items"])

    with table.batch_writer() as batch:
        for item in items:
            batch.delete_item(Key={pk_field: item[pk_field]})

    return len(items)


def clear_s3_parquet() -> int:
    """Borra los ficheros Parquet de las carpetas workouts/ y sleep/ en S3."""
    deleted = 0
    for prefix in ["workouts/", "sleep/"]:
        response = _s3.list_objects_v2(Bucket=config.S3_BUCKET, Prefix=prefix)
        for obj in response.get("Contents", []):
            if obj["Key"].endswith(".parquet"):
                _s3.delete_object(Bucket=config.S3_BUCKET, Key=obj["Key"])
                print(f"  Borrado S3: {obj['Key']}")
                deleted += 1
    return deleted


if __name__ == "__main__":
    print("Borrando datos anteriores...\n")

    n = clear_dynamo_table(config.DYNAMO_TABLE_WORKOUTS, "workout_id")
    print(f"[OK] DynamoDB {config.DYNAMO_TABLE_WORKOUTS}: {n} items borrados")

    n = clear_dynamo_table(config.DYNAMO_TABLE_SLEEP, "date")
    print(f"[OK] DynamoDB {config.DYNAMO_TABLE_SLEEP}: {n} items borrados")

    n = clear_s3_parquet()
    print(f"[OK] S3: {n} ficheros Parquet borrados")

    print("\nListo para cargar datos nuevos.")
