import os
import requests
import psycopg
import time
import schedule
from datetime import datetime

# -------------------------------
# Configuración de la base de datos
# -------------------------------
DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_NAME = os.environ.get("DB_NAME", "pruebadb")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

# -------------------------------
# Conexión a PostgreSQL
# -------------------------------
def get_connection():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

# -------------------------------
# Creación de tabla
# -------------------------------
def create_table():
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Crear tabla si no existe
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
        # Agregar columna fetched_at si no existe
        cur.execute("""
            ALTER TABLE valenbisi
            ADD COLUMN IF NOT EXISTS fetched_at TIMESTAMP;
        """)
        conn.commit()
        print("[INFO] Tabla valenbisi lista.")
    except Exception as e:
        print(f"[ERROR] No se pudo crear la tabla: {e}")
    finally:
        cur.close()
        conn.close()

# -------------------------------
# Descarga de datos desde API
# -------------------------------
def fetch_valenbisi(limit=100):
    url = (
        "https://valencia.opendatasoft.com/api/explore/v2.1/"
        "catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records"
    )
    params = {"limit": str(limit)}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.RequestException as e:
        print(f"[ERROR] Al descargar datos: {e}")
        return []

# -------------------------------
# Inserción de datos en PostgreSQL
# -------------------------------
def insert_valenbisi(data):
    if not data:
        print("[INFO] No hay datos nuevos.")
        return

    conn = get_connection()
    cur = conn.cursor()
    fetched_at = datetime.now()
    inserted = 0

    try:
        for station in data:
            geo = station.get("geo_point_2d", {})
            cur.execute("""
                INSERT INTO valenbisi (
                    address, number, open, available, free, total, ticket,
                    updated_at, lon, lat, update_jcd, fetched_at
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                station.get("address"),
                station.get("number"),
                station.get("open"),
                station.get("available"),
                station.get("free"),
                station.get("total"),
                station.get("ticket"),
                station.get("updated_at"),
                geo.get("lon"),
                geo.get("lat"),
                station.get("update_jcd"),
                fetched_at
            ))
            inserted += 1
        conn.commit()
        print(f"[INFO] {inserted} registros insertados a las {fetched_at}.")
    except Exception as e:
        print(f"[ERROR] Falló la inserción: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

# -------------------------------
# Trabajo programado
# -------------------------------
def job():
    print(f"[{datetime.now()}] Ejecutando ingesta Valenbisi...")
    data = fetch_valenbisi()
    insert_valenbisi(data)
    print(f"[{datetime.now()}] Ingesta finalizada.\n")

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    # Esperar que la base de datos esté lista
    time.sleep(5)
    create_table()
    job()

    # Ejecutar cada hora
    schedule.every().hour.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
