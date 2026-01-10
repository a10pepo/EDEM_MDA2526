import time
import requests
from datetime import datetime
import psycopg

STATION_INFO_URL = "https://valenbisi.com/gbfs/en/station_information.json"
STATION_STATUS_URL = "https://valenbisi.com/gbfs/en/station_status.json"

INTERVALO = 300  # 5 minutos

DB_CONFIG = {
    "dbname": "tu_base_de_datos",
    "user": "tu_usuario",
    "password": "tu_password",
    "host": "localhost",
    "port": 5432
}


def obtener_y_guardar_datos(conn):
    info = requests.get(STATION_INFO_URL).json()
    status = requests.get(STATION_STATUS_URL).json()

    estaciones_info = info["data"]["stations"]
    estaciones_status = status["data"]["stations"]

    status_dict = {
        est["station_id"]: est for est in estaciones_status
    }

    timestamp = datetime.now()

    insert_sql = """
        INSERT INTO valenbisi_raw (
            station_id,
            station_name,
            latitude,
            longitude,
            bikes_available,
            docks_available,
            station_status,
            query_timestamp
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    with conn.cursor() as cur:
        for estacion in estaciones_info:
            estado = status_dict.get(estacion["station_id"], {})

            cur.execute(
                insert_sql,
                (
                    estacion["station_id"],
                    estacion["name"],
                    estacion["lat"],
                    estacion["lon"],
                    estado.get("num_bikes_available"),
                    estado.get("num_docks_available"),
                    estado.get("status"),
                    timestamp
                )
            )

        conn.commit()


def main():
    print("🚲 Valenbisi collector iniciado")

    with psycopg.connect(**DB_CONFIG) as conn:
        while True:
            try:
                obtener_y_guardar_datos(conn)
                print("✔ Datos insertados correctamente")
            except Exception as e:
                print("❌ Error:", e)

            time.sleep(INTERVALO)


if __name__ == "__main__":
    main()
