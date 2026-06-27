"""Extrae entrenamientos de Garmin Connect y los carga en DynamoDB."""
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.workouts_extractor import load_workouts

if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    print(f"Extrayendo entrenamientos de los ultimos {days} dias...\n")
    count = load_workouts(days=days)
    print(f"\n[OK] {count} entrenamientos cargados en DynamoDB")
