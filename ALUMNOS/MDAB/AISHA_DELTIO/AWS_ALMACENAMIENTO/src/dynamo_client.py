"""
Cliente DynamoDB de escritura.
DynamoDB no acepta float nativo: la conversion pasa por JSON para
obtener Decimal de forma segura sin perder precision.
Los campos con valor None se omiten (DynamoDB no acepta null explicitamente).
"""
import json
import logging
from decimal import Decimal

import boto3
from src import config

logger = logging.getLogger(__name__)

_dynamodb = boto3.resource("dynamodb", region_name=config.AWS_REGION)


def _to_decimal(obj: dict) -> dict:
    # float -> Decimal via JSON: unico metodo seguro para todos los tipos anidados
    return json.loads(json.dumps(obj), parse_float=Decimal)


def put_item(table_name: str, item: dict) -> None:
    clean = {k: v for k, v in item.items() if v is not None}
    table = _dynamodb.Table(table_name)
    table.put_item(Item=_to_decimal(clean))
