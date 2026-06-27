"""Extrae metricas de sueno de Garmin Connect y las carga en DynamoDB."""
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.sleep_extractor import load_sleep

if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    print(f"Extrayendo sueno de los ultimos {days} dias...\n")
    count = load_sleep(days=days)
    print(f"\n[OK] {count} dias de sueno cargados en DynamoDB")
