import psycopg2
from psycopg2.extensions import connection as Connection

from config import DBConfig

# =============================================================================
# DDL — Relational schema (OLTP, 3NF)
# =============================================================================

CREATE_WORKOUTS = """
CREATE TABLE IF NOT EXISTS workouts (
    workout_id      SERIAL PRIMARY KEY,
    title           VARCHAR(255),
    start_time      TIMESTAMP,
    end_time        TIMESTAMP,
    description     TEXT,
    CONSTRAINT uq_workout UNIQUE (title, start_time)
);
"""

CREATE_EXERCISES = """
CREATE TABLE IF NOT EXISTS exercises (
    exercise_id     SERIAL PRIMARY KEY,
    exercise_title  VARCHAR(255) UNIQUE
);
"""

# NOTE: 'set' is a reserved SQL keyword, so the table is named 'sets'.
CREATE_SETS = """
CREATE TABLE IF NOT EXISTS sets (
    set_id           SERIAL PRIMARY KEY,
    workout_id       INT REFERENCES workouts(workout_id),
    exercise_id      INT REFERENCES exercises(exercise_id),
    superset_id      VARCHAR(50),
    exercise_notes   TEXT,
    set_index        INT,
    set_type         VARCHAR(50),
    weight_kg        NUMERIC(6, 2),
    reps             INT,
    distance_km      NUMERIC(6, 2),
    duration_seconds INT,
    rpe              NUMERIC(4, 2)
);
"""


def get_rds_connection(config: DBConfig) -> Connection:
    """Open and return a psycopg2 connection to the RDS PostgreSQL instance."""
    return psycopg2.connect(
        host=config.host,
        database=config.db,
        user=config.user,
        password=config.password,
        port=config.port,
    )


def create_rds_tables(conn: Connection) -> None:
    """Create the workouts/exercises/sets tables if they do not exist yet."""
    cursor = conn.cursor()
    try:
        cursor.execute(CREATE_WORKOUTS)
        cursor.execute(CREATE_EXERCISES)
        cursor.execute(CREATE_SETS)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()


# =============================================================================
# Redshift — analytical schema (denormalised, OLAP)
# =============================================================================

CREATE_FACT_SETS = """
CREATE TABLE IF NOT EXISTS fact_sets (
    set_id           INT,
    workout_id       INT,
    workout_title    VARCHAR(255),
    start_time       TIMESTAMP,
    end_time         TIMESTAMP,
    exercise_id      INT,
    exercise_title   VARCHAR(255),
    superset_id      VARCHAR(50),
    set_index        INT,
    set_type         VARCHAR(50),
    weight_kg        NUMERIC(6, 2),
    reps             INT,
    distance_km      NUMERIC(6, 2),
    duration_seconds INT,
    rpe              NUMERIC(4, 2)
)
DISTSTYLE EVEN
SORTKEY (start_time, workout_id);
"""


def get_redshift_connection(config: DBConfig) -> Connection:
    """Open and return a psycopg2 connection to the Redshift cluster."""
    return psycopg2.connect(
        host=config.host,
        database=config.db,
        user=config.user,
        password=config.password,
        port=config.port,
    )


def create_redshift_tables(redshift_conn: Connection) -> None:
    """Create the analytical fact_sets table in Redshift if it does not exist yet."""
    cursor = redshift_conn.cursor()
    try:
        cursor.execute(CREATE_FACT_SETS)
        redshift_conn.commit()
    except Exception:
        redshift_conn.rollback()
        raise
    finally:
        cursor.close()
