"""
load_rds.py — Load F1 data into RDS PostgreSQL.

Prerequisites:
  1. Run db/init.sql against your RDS instance to create tables:
       psql -h $PGHOST -U $PGUSER -d $PGDATABASE -f db/init.sql
  2. Copy .env.example to .env and fill in your RDS credentials.
  3. pip install -r requirements.txt

Run standalone:
  python src/load_rds.py

Environment variables (via .env or shell):
  PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE
"""

import sys
import os
import psycopg2
from dotenv import load_dotenv

from initial_info import teams, drivers, races

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.environ["PGHOST"],
        port=os.environ.get("PGPORT", 5432),
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        dbname=os.environ["PGDATABASE"],
    )


def insert_teams(cur):
    sql = """
        INSERT INTO teams (team_id, name, base, team_principal, power_unit, founded_year, championships)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (team_id) DO NOTHING
    """
    rows = [
        (t["teamId"], t["name"], t["base"], t["teamPrincipal"],
         t["powerUnit"], t["foundedYear"], t["championships"])
        for t in teams
    ]
    cur.executemany(sql, rows)
    return cur.rowcount


def insert_drivers(cur):
    sql = """
        INSERT INTO drivers (driver_id, team_id, code, name, nationality, date_of_birth, permanent_number)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (driver_id) DO NOTHING
    """
    rows = [
        (d["driverId"], d["teamId"], d["code"], d["name"],
         d["nationality"], d["dateOfBirth"], d["permanentNumber"])
        for d in drivers
    ]
    cur.executemany(sql, rows)
    return cur.rowcount


def insert_races(cur):
    sql = """
        INSERT INTO races (race_id, name, circuit, country, date, season, round, laps)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (race_id) DO NOTHING
    """
    rows = [
        (r["raceId"], r["name"], r["circuit"], r["country"],
         r["date"], r["season"], r["round"], r["laps"])
        for r in races
    ]
    cur.executemany(sql, rows)
    return cur.rowcount


def insert_results(cur):
    sql = """
        INSERT INTO results (race_id, driver_id, grid_position, final_position, points, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (race_id, driver_id) DO NOTHING
    """
    rows = []
    for race in races:
        for driver_id, grid, final, pts, status in race["results"]:
            rows.append((race["raceId"], driver_id, grid, final, pts, status))
    cur.executemany(sql, rows)
    return cur.rowcount


def main():
    try:
        conn = get_connection()
    except KeyError as e:
        print(f"Missing environment variable: {e}", file=sys.stderr)
        sys.exit(1)

    with conn:
        with conn.cursor() as cur:
            n_teams   = insert_teams(cur)
            n_drivers = insert_drivers(cur)
            n_races   = insert_races(cur)
            n_results = insert_results(cur)

    conn.close()

    print("RDS load complete:")
    print(f"  teams   : {n_teams}")
    print(f"  drivers : {n_drivers}")
    print(f"  races   : {n_races}")
    print(f"  results : {n_results}")


if __name__ == "__main__":
    main()
