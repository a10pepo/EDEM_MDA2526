from datetime import datetime

import pandas as pd
from psycopg2.extensions import connection as Connection


# =============================================================================
# Cleaning
# =============================================================================

def parse_hevy_date(date_str) -> datetime | None:
    """Parse Hevy date strings like '22 May 2026, 11:27' to datetime objects."""
    if pd.isna(date_str) or str(date_str).strip() == "":
        return None
    try:
        return datetime.strptime(str(date_str).strip(), "%d %b %Y, %H:%M")
    except ValueError:
        return None


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalise the raw CSV so psycopg2 can safely pass values to PostgreSQL:
    - NaN  -> None  (pandas sentinel is not accepted by psycopg2)
    - ""   -> None  (empty strings become SQL NULL, not empty text)
    - date columns are parsed to datetime objects
    """
    df["start_time"] = df["start_time"].apply(parse_hevy_date)
    df["end_time"] = df["end_time"].apply(parse_hevy_date)

    df = df.replace("", None)

    df = df.astype(object)
    df = df.where(pd.notnull(df), None)
    return df


# =============================================================================
# Insertion functions (dimension tables first, then fact table)
# =============================================================================

def _insert_workouts(cursor, df: pd.DataFrame) -> dict:
    """
    Upsert unique workout sessions into 'workouts'.
    Returns an in-memory map {(title, start_time_str): workout_id}.
    ON CONFLICT DO UPDATE ensures RETURNING always yields the current row id,
    even when the row already existed.
    """
    workout_map = {}
    unique_workouts = (
        df[["title", "start_time", "end_time", "description"]]
        .drop_duplicates(subset=["title", "start_time"])
    )

    for _, row in unique_workouts.iterrows():
        cursor.execute(
            """
            INSERT INTO workouts (title, start_time, end_time, description)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (title, start_time) DO UPDATE
                SET description = EXCLUDED.description
            RETURNING workout_id;
            """,
            (row["title"], row["start_time"], row["end_time"], row["description"]),
        )
        result = cursor.fetchone()
        if result:
            workout_map[(row["title"], str(row["start_time"]))] = result[0]

    return workout_map


def _insert_exercises(cursor, df: pd.DataFrame) -> dict:
    """
    Upsert unique exercises into 'exercises'.
    Returns an in-memory map {exercise_title: exercise_id}.
    """
    exercise_map = {}

    for ex_title in df["exercise_title"].dropna().unique():
        cursor.execute(
            """
            INSERT INTO exercises (exercise_title)
            VALUES (%s)
            ON CONFLICT (exercise_title) DO UPDATE
                SET exercise_title = EXCLUDED.exercise_title
            RETURNING exercise_id;
            """,
            (ex_title,),
        )
        result = cursor.fetchone()
        if result:
            exercise_map[ex_title] = result[0]

    return exercise_map


def _insert_sets(cursor, df: pd.DataFrame, workout_map: dict, exercise_map: dict) -> None:
    """
    Insert every row of the CSV into 'sets', resolving FKs from the
    in-memory maps built in the previous steps.
    Rows where either FK cannot be resolved are skipped and counted.
    """
    inserted = skipped = 0

    for _, row in df.iterrows():
        w_id = workout_map.get((row["title"], str(row["start_time"])))
        e_id = exercise_map.get(row["exercise_title"])

        if not (w_id and e_id):
            skipped += 1
            continue

        cursor.execute(
            """
            INSERT INTO sets (
                workout_id, exercise_id, superset_id, exercise_notes,
                set_index, set_type, weight_kg, reps,
                distance_km, duration_seconds, rpe
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                w_id,
                e_id,
                row["superset_id"],
                row["exercise_notes"],
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

    print(f"  Sets inserted: {inserted} | Skipped (unresolved FK): {skipped}")


def load_data(df: pd.DataFrame, conn: Connection) -> None:
    """Insert the cleaned dataframe into workouts, exercises and sets, in order."""
    cursor = conn.cursor()
    try:
        print("Inserting unique workouts...")
        workout_map = _insert_workouts(cursor, df)
        print(f"  Workouts processed: {len(workout_map)}")

        print("Inserting unique exercises...")
        exercise_map = _insert_exercises(cursor, df)
        print(f"  Exercises processed: {len(exercise_map)}")

        conn.commit()

        print("Inserting sets...")
        _insert_sets(cursor, df, workout_map, exercise_map)
        conn.commit()

    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
