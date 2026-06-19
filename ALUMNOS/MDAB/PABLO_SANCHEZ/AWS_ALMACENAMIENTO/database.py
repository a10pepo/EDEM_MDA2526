import os
import csv
import duckdb

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "futbolistas.duckdb")
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mejores_futbolistas.csv")


def get_conn():
    return duckdb.connect(DB_PATH)


def init_db():
    conn = get_conn()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS jugadores (
            id_jugador              VARCHAR PRIMARY KEY,
            Posicion                INTEGER,
            Nombre                  VARCHAR,
            Nacionalidad            VARCHAR,
            Club_Actual             VARCHAR,
            Edad                    INTEGER,
            Posicion_Campo          VARCHAR,
            Balones_de_Oro          INTEGER,
            fecha_nacimiento        VARCHAR,
            fecha_ultimo_partido    VARCHAR,
            fecha_proximo_partido   VARCHAR,
            salario_anual_millones  FLOAT,
            valor_mercado_millones  FLOAT,
            goles_temporada         INTEGER,
            asistencias_temporada   INTEGER,
            minutos_jugados         INTEGER,
            estado                  VARCHAR
        )
    """)

    if conn.execute("SELECT COUNT(*) FROM jugadores").fetchone()[0] == 0:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        conn.executemany(
            """INSERT INTO jugadores VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            [(
                r["id_jugador"],
                int(r["Posicion"]),
                r["Nombre"],
                r["Nacionalidad"],
                r["Club_Actual"],
                int(r["Edad"]),
                r["Posicion_Campo"],
                int(r["Balones_de_Oro"]),
                r["fecha_nacimiento"],
                r["fecha_ultimo_partido"],
                r["fecha_proximo_partido"],
                float(r["salario_anual_millones"]),
                float(r["valor_mercado_millones"]),
                int(r["goles_temporada"]),
                int(r["asistencias_temporada"]),
                int(r["minutos_jugados"]),
                r["estado"],
            ) for r in rows]
        )
        print(f"[DB] {len(rows)} jugadores cargados desde CSV.")

    conn.close()


def fetch_all(query, params=None):
    conn = get_conn()
    result = conn.execute(query, params or [])
    columns = [d[0] for d in result.description]
    rows = [dict(zip(columns, row)) for row in result.fetchall()]
    conn.close()
    return rows


def fetch_one(query, params=None):
    conn = get_conn()
    result = conn.execute(query, params or [])
    columns = [d[0] for d in result.description]
    row = result.fetchone()
    conn.close()
    return dict(zip(columns, row)) if row else None


def execute_write(query, params=None):
    conn = get_conn()
    conn.execute(query, params or [])
    conn.close()
