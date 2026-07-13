"""
Exporta datos de DynamoDB a S3 en formato Parquet y recrea las tablas en Athena.

Flujo: DynamoDB (scan) -> Parquet (pyarrow) -> S3 -> Athena DDL (DROP + CREATE)

Notas importantes:
  - El campo "date" de DynamoDB se renombra a workout_date/sleep_date para evitar
    conflictos con la palabra reservada DATE de SQL/Athena.
  - Las tablas Athena se recrean en cada exportacion para que el DDL
    siempre este sincronizado con el esquema real del Parquet.
"""
import io
import logging
import time
from decimal import Decimal

import boto3
import pyarrow as pa
import pyarrow.parquet as pq

from src import config

logger = logging.getLogger(__name__)

_dynamodb = boto3.resource("dynamodb", region_name=config.AWS_REGION)
_s3       = boto3.client("s3",         region_name=config.AWS_REGION)
_athena   = boto3.client("athena",     region_name=config.AWS_REGION)


# ── DynamoDB ──────────────────────────────────────────────────────────────────

def _decimal_to_float(obj):
    """Convierte recursivamente Decimal a float para serializar con pyarrow."""
    if isinstance(obj, list):
        return [_decimal_to_float(i) for i in obj]
    if isinstance(obj, dict):
        return {k: _decimal_to_float(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return float(obj)
    return obj


def _scan_table(table_name: str) -> list[dict]:
    """Lee todos los items de una tabla DynamoDB (paginacion automatica)."""
    table    = _dynamodb.Table(table_name)
    items    = []
    response = table.scan()
    items.extend(response["Items"])
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response["Items"])
    return _decimal_to_float(items)


# ── S3 ────────────────────────────────────────────────────────────────────────

def _upload_parquet(items: list[dict], s3_key: str) -> None:
    arrow_table = pa.Table.from_pylist(items)
    buf = io.BytesIO()
    pq.write_table(arrow_table, buf)
    buf.seek(0)
    _s3.put_object(Bucket=config.S3_BUCKET, Key=s3_key, Body=buf.getvalue())
    logger.info(f"Subido: s3://{config.S3_BUCKET}/{s3_key} ({len(items)} registros)")


# ── Athena ────────────────────────────────────────────────────────────────────

def _run_athena_query(sql: str) -> None:
    response = _athena.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={"Database": config.ATHENA_DATABASE},
        ResultConfiguration={"OutputLocation": config.ATHENA_RESULTS_PREFIX},
    )
    execution_id = response["QueryExecutionId"]
    while True:
        status = _athena.get_query_execution(QueryExecutionId=execution_id)
        state  = status["QueryExecution"]["Status"]["State"]
        if state in ("SUCCEEDED", "FAILED", "CANCELLED"):
            break
        time.sleep(1)
    if state != "SUCCEEDED":
        reason = status["QueryExecution"]["Status"].get("StateChangeReason", "")
        raise RuntimeError(f"Query Athena fallida ({state}): {reason}")


def _recreate_athena_tables() -> None:
    """Recrea ambas tablas externas en Athena apuntando al Parquet en S3."""

    _run_athena_query("DROP TABLE IF EXISTS workouts")
    _run_athena_query(f"""
        CREATE EXTERNAL TABLE workouts (
            workout_id            STRING,
            name                  STRING,
            type                  STRING,
            workout_date          STRING,
            start_time            STRING,
            duration_seconds      DOUBLE,
            distance_meters       DOUBLE,
            avg_hr                DOUBLE,
            max_hr                DOUBLE,
            calories              DOUBLE,
            avg_speed_ms          DOUBLE,
            elevation_gain        DOUBLE,
            training_effect       DOUBLE,
            anaerobic_effect      DOUBLE,
            training_stress_score DOUBLE,
            vo2max_value          DOUBLE,
            zone1_seconds         DOUBLE,
            zone2_seconds         DOUBLE,
            zone3_seconds         DOUBLE,
            zone4_seconds         DOUBLE,
            zone5_seconds         DOUBLE,
            temp_c                DOUBLE,
            feels_like_c          DOUBLE,
            humidity_pct          DOUBLE,
            precipitation_mm      DOUBLE,
            wind_speed_kmh        DOUBLE,
            body_battery_start    DOUBLE,
            body_battery_end      DOUBLE,
            body_battery_min      DOUBLE,
            body_battery_drop     DOUBLE,
            training_readiness    DOUBLE,
            stress_avg            DOUBLE
        )
        STORED AS PARQUET
        LOCATION 's3://{config.S3_BUCKET}/workouts/'
    """)
    logger.info("Tabla Athena 'workouts' recreada")

    _run_athena_query("DROP TABLE IF EXISTS sleep")
    _run_athena_query(f"""
        CREATE EXTERNAL TABLE sleep (
            sleep_date          STRING,
            sleep_start         STRING,
            sleep_end           STRING,
            total_sleep_seconds DOUBLE,
            deep_sleep_seconds  DOUBLE,
            light_sleep_seconds DOUBLE,
            rem_sleep_seconds   DOUBLE,
            awake_seconds       DOUBLE,
            avg_spo2            DOUBLE,
            avg_respiration     DOUBLE,
            resting_hr          DOUBLE,
            sleep_score         DOUBLE,
            hrv_avg             DOUBLE,
            hrv_5min_high       DOUBLE,
            hrv_status          STRING,
            hrv_baseline_low    DOUBLE,
            hrv_baseline_high   DOUBLE
        )
        STORED AS PARQUET
        LOCATION 's3://{config.S3_BUCKET}/sleep/'
    """)
    logger.info("Tabla Athena 'sleep' recreada")


# ── Punto de entrada ──────────────────────────────────────────────────────────

def export_all() -> None:
    """Ejecuta el pipeline completo: DynamoDB -> Parquet -> S3 -> Athena."""

    workouts = _scan_table(config.DYNAMO_TABLE_WORKOUTS)
    for w in workouts:
        # Renombrar "date" -> "workout_date" para evitar palabra reservada en SQL
        if "date" in w:
            w["workout_date"] = w.pop("date")
    _upload_parquet(workouts, "workouts/workouts.parquet")

    sleep = _scan_table(config.DYNAMO_TABLE_SLEEP)
    for s in sleep:
        if "date" in s:
            s["sleep_date"] = s.pop("date")
    _upload_parquet(sleep, "sleep/sleep.parquet")

    _recreate_athena_tables()
