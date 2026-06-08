import pandas as pd
from psycopg2.extensions import connection as Connection

# =============================================================================
# Extract — pull a denormalised view of the OLTP schema from RDS
# =============================================================================

EXTRACT_QUERY = """
SELECT
    s.set_id,
    w.workout_id,
    w.title          AS workout_title,
    w.start_time,
    w.end_time,
    e.exercise_id,
    e.exercise_title,
    s.superset_id,
    s.set_index,
    s.set_type,
    s.weight_kg,
    s.reps,
    s.distance_km,
    s.duration_seconds,
    s.rpe
FROM sets s
JOIN workouts w  ON w.workout_id = s.workout_id
JOIN exercises e ON e.exercise_id = s.exercise_id;
"""


def extract_from_rds(rds_conn: Connection) -> pd.DataFrame:
    """Read the joined workouts/exercises/sets data from RDS into a DataFrame."""
    return pd.read_sql(EXTRACT_QUERY, rds_conn)


# =============================================================================
# Load — insert the extracted rows into the Redshift fact table
# =============================================================================

def load_to_redshift(df: pd.DataFrame, redshift_conn: Connection) -> None:
    """Insert every row of the extracted DataFrame into Redshift's fact_sets table."""
    cursor = redshift_conn.cursor()
    inserted = 0
    df = df.astype(object).where(pd.notnull(df), None)
    try:
        for _, row in df.iterrows():
            cursor.execute(
                """
                INSERT INTO fact_sets (
                    set_id, workout_id, workout_title, start_time, end_time,
                    exercise_id, exercise_title, superset_id, set_index, set_type,
                    weight_kg, reps, distance_km, duration_seconds, rpe
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    row["set_id"],
                    row["workout_id"],
                    row["workout_title"],
                    row["start_time"],
                    row["end_time"],
                    row["exercise_id"],
                    row["exercise_title"],
                    row["superset_id"],
                    row["set_index"],
                    row["set_type"],
                    row["weight_kg"],
                    row["reps"],
                    row["distance_km"],
                    row["duration_seconds"],
                    row["rpe"],
                ),
            )
            inserted += 1

        redshift_conn.commit()
        print(f"  Rows loaded into Redshift: {inserted}")

    except Exception:
        redshift_conn.rollback()
        raise
    finally:
        cursor.close()


def run_el(rds_conn: Connection, redshift_conn: Connection) -> None:
    """Extract from RDS and load into Redshift, end to end."""
    print("Extracting data from RDS...")
    df = extract_from_rds(rds_conn)
    print(f"  {len(df)} rows extracted.")

    print("Loading data into Redshift...")
    load_to_redshift(df, redshift_conn)
