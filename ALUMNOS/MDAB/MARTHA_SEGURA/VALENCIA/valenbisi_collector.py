import os
import time
from datetime import datetime
import requests
import psycopg2


# CONFIGURACIÓN API

BASE_URL = (
    "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
    "valenbisi-disponibilitat-valenbisi-dsiponibilidad/records"
)
LIMIT = 100  
POLL_SECONDS = 300


# FUNCIONES API
def fetch_valenbisi(offset):
    url = f"{BASE_URL}?limit={LIMIT}&offset={offset}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def parse_stations(payload):
    timestamp = datetime.now()
    rows = []

    for s in payload["results"]:
        geo = s["geo_point_2d"]

        row = {
            "station_id": s["number"],
            "station_name": s["address"],
            "latitude": geo["lat"],
            "longitude": geo["lon"],
            "available_bikes": s["available"],
            "available_slots": s["free"],
            "station_status": s["open"],
            "total_capacity": s["total"],
            "timestamp": timestamp
        }
        rows.append(row)

    return rows


# POSTGRES

def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "valenbisi_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


def insert_rows(rows):
    sql = """
        INSERT INTO valenbisi_raw
        (station_id, station_name, latitude, longitude,
         available_bikes, available_slots, station_status,
         total_capacity, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = []
    for r in rows:
        values.append(
            (
                r["station_id"],
                r["station_name"],
                r["latitude"],
                r["longitude"],
                r["available_bikes"],
                r["available_slots"],
                r["station_status"],
                r["total_capacity"],
                r["timestamp"],
            )
        )

    conn = get_conn()
    cur = conn.cursor()
    cur.executemany(sql, values)
    conn.commit()
    cur.close()
    conn.close()


# MAIN (cada 5 minutos)

if __name__ == "__main__":
    print("[INFO] Iniciando collector de Valenbisi")

    while True:
        offset = 0
        total_inserted = 0

        while True:
            data = fetch_valenbisi(offset)
            rows = parse_stations(data)

            if len(rows) == 0:
                break

            insert_rows(rows)
            total_inserted += len(rows)

            if len(rows) < LIMIT:
                break

            offset += LIMIT

        print(
            f"[OK] {total_inserted} filas insertadas "
            f"a las {datetime.now()}"
        )

        print(f"[INFO] Esperando {POLL_SECONDS} segundos...\n")
        time.sleep(POLL_SECONDS)





