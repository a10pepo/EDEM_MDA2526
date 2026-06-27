"""
Pipeline completo: Garmin Connect -> DynamoDB -> S3 (Parquet) -> Athena.

Uso:
    python main.py                     # carga ultimos 30 dias
    python main.py --days 60           # carga ultimos 60 dias
    python main.py --reset             # borra datos anteriores y recarga
    python main.py --reset --days 60   # reset + 60 dias
    python main.py --pdf               # genera PDF al finalizar
"""
import sys
import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

from src.workouts_extractor import load_workouts
from src.sleep_extractor import load_sleep
from src.s3_loader import export_all


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline Garmin -> AWS")
    parser.add_argument("--days",  type=int, default=30, help="Dias a cargar (default: 30)")
    parser.add_argument("--reset", action="store_true", help="Borrar datos previos antes de cargar")
    parser.add_argument("--pdf",   action="store_true", help="Generar informe PDF al finalizar")
    args = parser.parse_args()

    if args.reset:
        from scripts.reset_data import clear_dynamo_table, clear_s3_parquet
        from src import config
        print("\nBorrando datos anteriores...")
        n = clear_dynamo_table(config.DYNAMO_TABLE_WORKOUTS, "workout_id")
        print(f"  DynamoDB {config.DYNAMO_TABLE_WORKOUTS}: {n} items borrados")
        n = clear_dynamo_table(config.DYNAMO_TABLE_SLEEP, "date")
        print(f"  DynamoDB {config.DYNAMO_TABLE_SLEEP}: {n} items borrados")
        n = clear_s3_parquet()
        print(f"  S3: {n} ficheros Parquet borrados")

    print(f"\nCargando entrenamientos ({args.days} dias)...")
    n_workouts = load_workouts(days=args.days)
    print(f"  [OK] {n_workouts} entrenamientos cargados en DynamoDB")

    print(f"\nCargando sueno ({args.days} dias)...")
    n_sleep = load_sleep(days=args.days)
    print(f"  [OK] {n_sleep} dias de sueno cargados en DynamoDB")

    print("\nExportando a S3 y recreando tablas Athena...")
    export_all()
    print("  [OK] Datos listos en Athena (tablas: workouts, sleep)")

    if args.pdf:
        import subprocess
        print("\nGenerando informe PDF...")
        result = subprocess.run([sys.executable, "scripts/generar_pdf.py"])
        if result.returncode != 0:
            print("  [FAIL] Error al generar el PDF")


if __name__ == "__main__":
    main()
