import os
import time
import math
import psycopg2

DB_HOST     = os.environ["DB_HOST"]
DB_PORT     = os.environ.get("DB_PORT", "5432")
DB_NAME     = os.environ["DB_NAME"]
DB_USER     = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

STEP     = 0.01
TICK     = 5
MIN_DIST = 0.01


def distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    return math.sqrt((lat2 - lat1) ** 2 + (lng2 - lng1) ** 2)


def interpolate_step(act_lat: float, act_lng: float,
                     dest_lat: float, dest_lng: float) -> tuple[float, float]:
    return (
        act_lat + (dest_lat - act_lat) * STEP,
        act_lng + (dest_lng - act_lng) * STEP,
    )


def tick(conn) -> None:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, origen_lat, origen_lng, destino_lat, destino_lng, actual_lat, actual_lng
            FROM rutas WHERE estado = 'en_ruta'
        """)
        for row in cur.fetchall():
            route_id, orig_lat, orig_lng, dest_lat, dest_lng, act_lat, act_lng = row
            act_lat, act_lng   = float(act_lat),  float(act_lng)
            dest_lat, dest_lng = float(dest_lat), float(dest_lng)
            orig_lat, orig_lng = float(orig_lat), float(orig_lng)

            if distance(act_lat, act_lng, dest_lat, dest_lng) < MIN_DIST:
                cur.execute("UPDATE rutas SET estado = 'completada' WHERE id = %s", (route_id,))
                cur.execute("""
                    INSERT INTO rutas
                        (vehiculo_id, conductor_id, origen_lat, origen_lng,
                         destino_lat, destino_lng, actual_lat, actual_lng, estado)
                    SELECT vehiculo_id, conductor_id,
                           destino_lat, destino_lng,
                           origen_lat,  origen_lng,
                           destino_lat, destino_lng,
                           'en_ruta'
                    FROM rutas WHERE id = %s
                """, (route_id,))
            else:
                new_lat, new_lng = interpolate_step(act_lat, act_lng, dest_lat, dest_lng)
                cur.execute(
                    "UPDATE rutas SET actual_lat = %s, actual_lng = %s WHERE id = %s",
                    (new_lat, new_lng, route_id),
                )
        conn.commit()


def main() -> None:
    print("Simulator starting...")
    conn = None
    while True:
        try:
            if conn is None or conn.closed:
                conn = psycopg2.connect(
                    host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
                    user=DB_USER, password=DB_PASSWORD,
                )
                print("DB connected")
            tick(conn)
        except Exception as exc:
            print(f"Error: {exc}")
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass
            conn = None
            time.sleep(5)
        else:
            time.sleep(TICK)


if __name__ == "__main__":
    main()
