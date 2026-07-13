"""Configuración centralizada leída de variables de entorno (.env)."""
import os

from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")

# Base de datos transaccional: PostgreSQL en RDS
PG = {
    "host": os.getenv("PG_HOST", "localhost"),
    "port": int(os.getenv("PG_PORT", "5432")),
    "dbname": os.getenv("PG_DB", "aviation"),
    "user": os.getenv("PG_USER", "postgres"),
    "password": os.getenv("PG_PASSWORD", "postgres"),
}

# Base de datos analítica: Redshift (habla el protocolo de PostgreSQL)
REDSHIFT = {
    "host": os.getenv("RS_HOST", ""),
    "port": int(os.getenv("RS_PORT", "5439")),
    "dbname": os.getenv("RS_DB", "analytics"),
    "user": os.getenv("RS_USER", "admin"),
    "password": os.getenv("RS_PASSWORD", ""),
}

# Data lakehouse: Iceberg + S3 + Glue
S3_BUCKET = os.getenv("S3_BUCKET", "")
GLUE_DATABASE = os.getenv("GLUE_DATABASE", "aviation_lakehouse")
ICEBERG_WAREHOUSE = os.getenv("ICEBERG_WAREHOUSE") or f"s3://{S3_BUCKET}/warehouse"
