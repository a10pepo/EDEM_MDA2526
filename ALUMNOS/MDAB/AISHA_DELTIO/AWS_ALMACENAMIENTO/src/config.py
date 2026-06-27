"""
Carga y valida todas las variables de entorno desde el fichero .env.
Lanza EnvironmentError al arrancar si falta alguna variable requerida,
para detectar errores de configuracion antes de tocar AWS o Garmin.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"Variable de entorno requerida no definida: {key}")
    return value


# AWS
AWS_REGION = _require("AWS_REGION")

# Garmin Connect
GARMIN_EMAIL    = _require("GARMIN_EMAIL")
GARMIN_PASSWORD = _require("GARMIN_PASSWORD")

# DynamoDB — almacenamiento primario (PAY_PER_REQUEST, sin coste fijo)
DYNAMO_TABLE_WORKOUTS = _require("DYNAMO_TABLE_WORKOUTS")
DYNAMO_TABLE_SLEEP    = _require("DYNAMO_TABLE_SLEEP")

# S3 + Athena — analitica sin servidor (~0 EUR/mes a este volumen de datos)
S3_BUCKET             = _require("S3_BUCKET")
ATHENA_DATABASE       = _require("ATHENA_DATABASE")
ATHENA_RESULTS_PREFIX = _require("ATHENA_RESULTS_PREFIX")

# Ubicacion para datos meteorologicos (Open-Meteo, gratuito)
LOCATION_LAT = float(_require("LOCATION_LAT"))
LOCATION_LON = float(_require("LOCATION_LON"))
LOCATION_TZ  = _require("LOCATION_TZ")
