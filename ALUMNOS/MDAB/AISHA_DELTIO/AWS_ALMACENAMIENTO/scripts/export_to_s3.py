"""Exporta datos de DynamoDB a S3 como Parquet y crea tablas en Athena."""
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.s3_loader import export_all

if __name__ == "__main__":
    print("Exportando DynamoDB -> S3 (Parquet)...\n")
    export_all()
    print("\n[OK] Datos listos en Athena")
    print("  Base de datos : garmin_db")
    print("  Tablas        : workouts, sleep")
