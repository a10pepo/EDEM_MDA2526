"""Verifica la conexion con Garmin Connect."""
import sys
import os
import logging
from datetime import date

logging.basicConfig(level=logging.WARNING)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.garmin_client import get_client

try:
    client = get_client()
    full_name = client.get_full_name()
    print(f"[OK] Conectado a Garmin Connect como: {full_name}")

    today = date.today().isoformat()
    stats = client.get_stats(today)
    print(f"[OK] Pasos hoy: {stats.get('totalSteps', 'N/A')}")
    print(f"[OK] Calorias hoy: {stats.get('totalKilocalories', 'N/A')}")
    print("\nConexion verificada. Listo para extraer datos.")
except Exception as e:
    print(f"[FAIL] Error al conectar con Garmin: {e}")
    sys.exit(1)
