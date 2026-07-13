"""
Diagnostico de configuracion: verifica que todas las conexiones esten operativas.
Util para comprobar el entorno antes de ejecutar el pipeline.

Uso: python scripts/check_config.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    import src.config as config
    print("[OK] Variables de entorno cargadas correctamente")
    print(f"  AWS_REGION:              {config.AWS_REGION}")
    print(f"  GARMIN_EMAIL:            {config.GARMIN_EMAIL}")
    print(f"  DYNAMO_TABLE_WORKOUTS:   {config.DYNAMO_TABLE_WORKOUTS}")
    print(f"  DYNAMO_TABLE_SLEEP:      {config.DYNAMO_TABLE_SLEEP}")
    print(f"  S3_BUCKET:               {config.S3_BUCKET}")
    print(f"  ATHENA_DATABASE:         {config.ATHENA_DATABASE}")
    print(f"  ATHENA_RESULTS_PREFIX:   {config.ATHENA_RESULTS_PREFIX}")
except EnvironmentError as e:
    print(f"[FAIL] Error de configuracion: {e}")
    sys.exit(1)

import boto3

try:
    sts      = boto3.client("sts", region_name=config.AWS_REGION)
    identity = sts.get_caller_identity()
    print(f"\n[OK] Credenciales AWS validas")
    print(f"  Account: {identity['Account']}")
    print(f"  UserId:  {identity['UserId']}")
except Exception as e:
    print(f"\n[FAIL] Error de credenciales AWS: {e}")
    sys.exit(1)

try:
    dynamodb = boto3.client("dynamodb", region_name=config.AWS_REGION)
    tables   = dynamodb.list_tables()["TableNames"]
    for expected in [config.DYNAMO_TABLE_WORKOUTS, config.DYNAMO_TABLE_SLEEP]:
        if expected in tables:
            print(f"[OK] Tabla DynamoDB encontrada: {expected}")
        else:
            print(f"[FAIL] Tabla DynamoDB NO encontrada: {expected}")
except Exception as e:
    print(f"[FAIL] Error al conectar con DynamoDB: {e}")
    sys.exit(1)

try:
    s3 = boto3.client("s3", region_name=config.AWS_REGION)
    s3.head_bucket(Bucket=config.S3_BUCKET)
    print(f"[OK] Bucket S3 accesible: {config.S3_BUCKET}")
except Exception as e:
    print(f"[FAIL] Error al acceder al bucket S3: {e}")
    sys.exit(1)

try:
    athena = boto3.client("athena", region_name=config.AWS_REGION)
    athena.get_database(CatalogName="AwsDataCatalog", DatabaseName=config.ATHENA_DATABASE)
    print(f"[OK] Base de datos Athena encontrada: {config.ATHENA_DATABASE}")
except Exception as e:
    print(f"[FAIL] Error al conectar con Athena: {e}")
    sys.exit(1)

print("\nTodo correcto. Puedes ejecutar: python main.py")
