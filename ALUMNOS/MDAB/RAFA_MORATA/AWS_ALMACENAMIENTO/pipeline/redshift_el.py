"""EL: extrae de PostgreSQL (RDS) y carga en Redshift (analítica).

Es un EL puro (Extract + Load): se replica la estructura sin transformar.
Para este volumen se usan INSERT por lotes. Para grandes volúmenes lo
recomendable sería descargar a S3 y usar el comando COPY de Redshift.
"""
import os

from psycopg2.extras import execute_values

from . import db

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema", "redshift.sql")

# Orden de columnas por tabla (debe coincidir en origen y destino)
COLUMNS = {
    "airplanes": [
        "plate_number", "type", "last_maintenance_date", "next_maintenance_date",
        "capacity", "owner_id", "owner_name", "hangar_id", "fuel_capacity",
    ],
    "passengers": ["passenger_id", "name", "national_id", "date_of_birth"],
    "flights": [
        "flight_id", "plate_number", "arrival_time", "departure_time",
        "fuel_consumption", "occupied_seats", "origin", "destination",
    ],
    "flight_passengers": ["flight_id", "passenger_id", "status"],
}

# Cargar respetando las FK: primero las tablas padre
LOAD_ORDER = ["airplanes", "passengers", "flights", "flight_passengers"]


def run():
    with open(SCHEMA_FILE, encoding="utf-8") as f:
        schema_sql = f.read()

    source = db.connect_postgres()
    target = db.connect_redshift()
    try:
        with target.cursor() as cur:
            cur.execute(schema_sql)
        target.commit()

        for table in LOAD_ORDER:
            cols = COLUMNS[table]
            rows = db.fetch_dicts(source, table)
            values = [tuple(r[c] for c in cols) for r in rows]

            with target.cursor() as cur:
                cur.execute(f"TRUNCATE TABLE {table}")
                if values:
                    execute_values(
                        cur,
                        f"INSERT INTO {table} ({', '.join(cols)}) VALUES %s",
                        values,
                    )
            target.commit()
            print(f"[redshift] {table}: {len(values)} filas cargadas.")
    finally:
        source.close()
        target.close()


if __name__ == "__main__":
    run()
