import os
import psycopg2
import psycopg2.extras
from datetime import date
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Gestor F1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

RECORD_WINS = 103


def get_conn():
    return psycopg2.connect(
        host=os.environ['RDS_HOST'],
        port=os.environ['RDS_PORT'],
        user=os.environ['RDS_USER'],
        password=os.environ['RDS_PASSWORD'],
        database=os.environ['RDS_DB'],
    )


# --- MODELOS ---

class Pilot(BaseModel):
    rank: int
    driver: str
    nationality: str
    wins: int
    championships: int
    years_active: str
    team_most_wins_with: str


class Race(BaseModel):
    race_id: str
    name: str
    circuit: str
    date: str
    laps: int
    total_distance_km: int


class Result(BaseModel):
    result_id: str
    race_id: str
    driver: str
    position: int
    points: int
    status: str


# --- LISTADOS ---

@app.get("/pilots")
def list_pilots():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM pilots ORDER BY rank;")
        return cur.fetchall()


@app.get("/races")
def list_races():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM races ORDER BY date;")
        return cur.fetchall()


@app.get("/results")
def list_results():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM results ORDER BY result_id;")
        return cur.fetchall()


# --- REGISTRO ---

@app.post("/pilots", status_code=201)
def register_pilot(p: Pilot):
    with get_conn() as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO pilots VALUES (%s,%s,%s,%s,%s,%s,%s);",
                        (p.rank, p.driver, p.nationality, p.wins, p.championships, p.years_active, p.team_most_wins_with))
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"message": f"Piloto {p.driver} registrado correctamente."}


@app.post("/races", status_code=201)
def register_race(r: Race):
    with get_conn() as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO races VALUES (%s,%s,%s,%s,%s,%s);",
                        (r.race_id, r.name, r.circuit, r.date, r.laps, r.total_distance_km))
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"message": f"Carrera {r.name} registrada correctamente."}


@app.post("/results", status_code=201)
def register_result(r: Result):
    with get_conn() as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO results VALUES (%s,%s,%s,%s,%s,%s);",
                        (r.result_id, r.race_id, r.driver, r.position, r.points, r.status))
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"message": f"Resultado {r.result_id} registrado correctamente."}


# --- CONSULTAS ---

@app.get("/pilots/days-since-race")
def days_since_last_race():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT p.driver,
                   CURRENT_DATE - MAX(r.date) AS days_since
            FROM pilots p
            LEFT JOIN results res ON p.driver = res.driver
            LEFT JOIN races r ON res.race_id = r.race_id
            GROUP BY p.driver
            ORDER BY days_since DESC NULLS FIRST;
        """)
        return cur.fetchall()


@app.get("/pilots/wins-to-record")
def wins_to_record():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(f"SELECT driver, wins, {RECORD_WINS} - wins AS wins_needed FROM pilots ORDER BY rank;")
        return cur.fetchall()


@app.get("/pilots/status")
def pilot_status():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT driver, years_active,
                   CASE WHEN years_active LIKE '%present%' THEN 'Activo' ELSE 'Retirado' END AS status
            FROM pilots ORDER BY rank;
        """)
        return cur.fetchall()


# --- ALERTAS ---

@app.get("/alerts/high-dnf-rate")
def alert_high_dnf_rate():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT driver, COUNT(*) AS total,
                   SUM(CASE WHEN status = 'DNF' THEN 1 ELSE 0 END) AS dnfs,
                   round(SUM(CASE WHEN status = 'DNF' THEN 1 ELSE 0 END)::numeric / COUNT(*) * 100, 1) AS dnf_pct
            FROM results
            GROUP BY driver
            HAVING SUM(CASE WHEN status = 'DNF' THEN 1 ELSE 0 END)::float / COUNT(*) > 0.10
            ORDER BY dnf_pct DESC;
        """)
        return cur.fetchall()


@app.get("/alerts/retired-pilots")
def alert_retired_pilots():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT driver, years_active FROM pilots WHERE years_active NOT LIKE '%present%' ORDER BY rank;")
        return cur.fetchall()


@app.get("/alerts/dominant-pilots")
def alert_dominant_pilots():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(f"""
            SELECT driver, wins,
                   round(wins::numeric / {RECORD_WINS} * 100, 1) AS pct
            FROM pilots
            WHERE wins::float / {RECORD_WINS} >= 0.10
            ORDER BY wins DESC;
        """)
        return cur.fetchall()


# --- ESTADISTICAS ---

@app.get("/stats/points-per-pilot")
def stats_points_per_pilot():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT driver,
                   COUNT(*) AS races,
                   SUM(points) AS total_points,
                   SUM(CASE WHEN position = 1 THEN 1 ELSE 0 END) AS wins,
                   round(AVG(points), 1) AS avg_points
            FROM results
            GROUP BY driver
            ORDER BY total_points DESC;
        """)
        return cur.fetchall()


@app.get("/stats/wins-per-circuit")
def stats_wins_per_circuit():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT r.circuit, COUNT(*) AS total_races
            FROM races r
            GROUP BY r.circuit
            ORDER BY total_races DESC;
        """)
        return cur.fetchall()


@app.get("/stats/summary")
def stats_summary():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT COUNT(*) AS total FROM pilots;")
        total_pilots = cur.fetchone()["total"]
        cur.execute("SELECT COUNT(*) AS total FROM races;")
        total_races = cur.fetchone()["total"]
        cur.execute("SELECT COUNT(*) AS total FROM results;")
        total_results = cur.fetchone()["total"]
        cur.execute("SELECT driver FROM results WHERE position = 1 GROUP BY driver ORDER BY COUNT(*) DESC LIMIT 1;")
        top = cur.fetchone()
        return {
            "total_pilots": total_pilots,
            "total_races": total_races,
            "total_results": total_results,
            "most_wins_driver": top["driver"] if top else "-"
        }
