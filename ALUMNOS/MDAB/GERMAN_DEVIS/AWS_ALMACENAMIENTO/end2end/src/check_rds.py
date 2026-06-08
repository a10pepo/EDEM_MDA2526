import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.environ["PGHOST"],
    port=os.environ.get("PGPORT", 5432),
    user=os.environ["PGUSER"],
    password=os.environ["PGPASSWORD"],
    dbname=os.environ["PGDATABASE"],
)

with conn.cursor() as cur:
    cur.execute(
        "SELECT race_id, driver_id, grid_position, final_position, points, status "
        "FROM results ORDER BY race_id, final_position"
    )
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    print(" | ".join(f"{c:20}" for c in cols))
    print("-" * (23 * len(cols)))
    for row in rows:
        print(" | ".join(f"{str(v):20}" for v in row))

conn.close()
