from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


def get_conn():
    return psycopg2.connect(
        host=os.environ["PGHOST"],
        port=os.environ.get("PGPORT", 5432),
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        dbname=os.environ["PGDATABASE"],
    )


def query(sql):
    conn = get_conn()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/teams")
def get_teams():
    return query("SELECT * FROM teams ORDER BY name")


@app.get("/drivers")
def get_drivers():
    return query("""
        SELECT d.driver_id, d.code, d.name, d.nationality, d.date_of_birth,
               d.permanent_number, t.name AS team
        FROM drivers d
        JOIN teams t ON d.team_id = t.team_id
        ORDER BY d.code
    """)


@app.get("/races")
def get_races():
    return query("SELECT * FROM races ORDER BY season, round")


@app.get("/results")
def get_results():
    return query("""
        SELECT r.race_id, rc.name AS race, d.code AS driver,
               d.name AS driver_name, r.grid_position, r.final_position,
               r.points, r.status
        FROM results r
        JOIN races rc ON r.race_id = rc.race_id
        JOIN drivers d ON r.driver_id = d.driver_id
        ORDER BY rc.season, rc.round, r.final_position
    """)
