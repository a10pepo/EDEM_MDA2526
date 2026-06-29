"""Conexiones a las bases de datos y utilidades de extracción."""
import psycopg2

from . import config


def connect_postgres():
    """Conexión a PostgreSQL (RDS), la BBDD transaccional (origen)."""
    return psycopg2.connect(
        host=config.PG["host"],
        port=config.PG["port"],
        dbname=config.PG["dbname"],
        user=config.PG["user"],
        password=config.PG["password"],
    )


def connect_redshift():
    """Conexión a Redshift (analítica). Requiere SSL."""
    c = config.REDSHIFT
    return psycopg2.connect(
        host=c["host"],
        port=c["port"],
        dbname=c["dbname"],
        user=c["user"],
        password=c["password"],
        sslmode="require",
    )


def fetch_dicts(conn, table):
    """Extrae todas las filas de una tabla como lista de diccionarios."""
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {table}")
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
