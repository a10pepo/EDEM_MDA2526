import os
import requests
import psycopg
from time import sleep

# -----------------------------
# Variables de entorno
# -----------------------------
DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_NAME = os.environ.get("DB_NAME", "pruebadb")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

# -----------------------------
# Espera a que Postgres arranque
# -----------------------------
sleep(5)

# -----------------------------
# Conexión usando psycopg3
# -----------------------------
conn = psycopg.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
)

cur = conn.cursor()

# -----------------------------
# Crear tabla si no existe
# -----------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS valenbisi (
    address TEXT,
    number INT,
    open TEXT,
    available INT,
    free INT,
    total INT,
    ticket TEXT,
    updated_at TEXT,
    lon DOUBLE PRECISION,
    lat DOUBLE PRECISION,
    update_jcd TEXT
);
""")
conn.commit()

# -----------------------------
# Función para descargar datos
# -----------------------------
def fetch_valenbisi(limit=20, offset=0):
    url = (
        "https://valencia.opendatasoft.com/api/explore/v2.1/"
        "catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records"
    )
    params = {"limit": str(limit), "offset": str(offset)}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("results", [])

# -----------------------------
# Script principal
# -----------------------------
if __name__ == "__main__":
    valenbisi_data = fetch_valenbisi(limit=20)

    if not valenbisi_data:
        print("No se han descargado registros.")
    else:
        print(f"Se han descargado {len(valenbisi_data)} registros.\n")

        for i, station in enumerate(valenbisi_data, start=1):
            print(f"Estación {i}: {station.get('address')} - Available: {station.get('available')}")

            cur.execute("""
                INSERT INTO valenbisi (
                    address, number, open, available, free, total, ticket,
                    updated_at, lon, lat, update_jcd
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                station.get("address"),
                station.get("number"),
                station.get("open"),
                station.get("available"),
                station.get("free"),
                station.get("total"),
                station.get("ticket"),
                station.get("updated_at"),
                station.get("geo_point_2d", {}).get("lon"),
                station.get("geo_point_2d", {}).get("lat"),
                station.get("update_jcd"),
            ))

        conn.commit()
        print("\nDatos insertados correctamente en PostgreSQL.")

        # Cerrar cursor y conexión
        cur.close()
        conn.close()
