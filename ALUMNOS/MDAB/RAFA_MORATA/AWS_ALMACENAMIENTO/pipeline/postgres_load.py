"""Crea el modelo transaccional en PostgreSQL (RDS) y carga `initial_info`."""
import os

from psycopg2.extras import execute_values

from . import data, db

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema", "postgres.sql")


def run():
    with open(SCHEMA_FILE, encoding="utf-8") as f:
        schema_sql = f.read()

    conn = db.connect_postgres()
    try:
        with conn.cursor() as cur:
            cur.execute(schema_sql)

            execute_values(
                cur,
                "INSERT INTO airplanes (plate_number, type, last_maintenance_date, "
                "next_maintenance_date, capacity, owner_id, owner_name, hangar_id, "
                "fuel_capacity) VALUES %s ON CONFLICT (plate_number) DO NOTHING",
                data.airplane_rows(),
            )
            execute_values(
                cur,
                "INSERT INTO passengers (passenger_id, name, national_id, "
                "date_of_birth) VALUES %s ON CONFLICT (passenger_id) DO NOTHING",
                data.passenger_rows(),
            )
            execute_values(
                cur,
                "INSERT INTO flights (flight_id, plate_number, arrival_time, "
                "departure_time, fuel_consumption, occupied_seats, origin, "
                "destination) VALUES %s ON CONFLICT (flight_id) DO NOTHING",
                data.flight_rows(),
            )
            execute_values(
                cur,
                "INSERT INTO flight_passengers (flight_id, passenger_id, status) "
                "VALUES %s ON CONFLICT (flight_id, passenger_id) DO NOTHING",
                data.flight_passenger_rows(),
            )
        conn.commit()
        print(
            "[postgres] Esquema creado y datos cargados en RDS: "
            f"{len(data.airplane_rows())} aviones, "
            f"{len(data.passenger_rows())} pasajeros, "
            f"{len(data.flight_rows())} vuelos, "
            f"{len(data.flight_passenger_rows())} relaciones vuelo-pasajero."
        )
    finally:
        conn.close()


if __name__ == "__main__":
    run()
