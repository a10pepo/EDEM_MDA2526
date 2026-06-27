"""
Analisis de como los entrenamientos afectan al sueno.
Une workout del dia N con el sueno de la noche N->N+1.
"""
import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import boto3
from src import config

_athena = boto3.client("athena", region_name=config.AWS_REGION)

# En Garmin, sleep_date = dia en que te despiertas.
# Si entrenas el dia N y duermes esa noche, el registro es sleep_date = N+1.
JOIN_CONDITION = """
    JOIN sleep s
      ON s.sleep_date = date_format(
            date_add('day', 1, date_parse(w.workout_date, '%Y-%m-%d')),
            '%Y-%m-%d'
         )
"""

QUERIES = {

    "Entrenamiento vs sueno esa noche (tabla completa)": f"""
        SELECT
            w.workout_date                                              AS fecha,
            w.type                                                      AS tipo,
            w.name                                                      AS nombre,
            HOUR(date_parse(substr(w.start_time,1,19), '%Y-%m-%d %H:%i:%s'))
                                                                        AS hora_inicio,
            ROUND(w.duration_seconds / 60)                             AS duracion_min,
            CAST(w.avg_hr  AS INTEGER)                                  AS fc_media,
            CAST(w.max_hr  AS INTEGER)                                  AS fc_max,
            ROUND(w.training_effect,   1)                              AS efecto_aerobico,
            ROUND(w.anaerobic_effect,  1)                              AS efecto_anaerobico,
            CAST(COALESCE(w.zone4_seconds, 0) / 60 AS INTEGER)        AS min_zona4,
            CAST(COALESCE(w.zone5_seconds, 0) / 60 AS INTEGER)        AS min_zona5,
            date_diff('minute',
                date_add('second',
                    CAST(w.duration_seconds AS INTEGER),
                    date_parse(substr(w.start_time,1,19), '%Y-%m-%d %H:%i:%s')
                ),
                date_parse(substr(s.sleep_start,1,19), '%Y-%m-%dT%H:%i:%s')
            )                                                           AS min_fin_a_dormir,
            CAST(s.sleep_score AS INTEGER)                             AS score_sueno,
            ROUND(s.total_sleep_seconds / 3600.0, 1)                  AS horas_sueno,
            CAST(s.hrv_avg AS INTEGER)                                 AS hrv,
            s.hrv_status                                               AS hrv_estado,
            ROUND(s.deep_sleep_seconds  / 3600.0, 1)                  AS profundo_h,
            ROUND(s.rem_sleep_seconds   / 3600.0, 1)                  AS rem_h
        FROM workouts w
        {JOIN_CONDITION}
        ORDER BY w.workout_date DESC
    """,

    "Hora del entrenamiento vs calidad del sueno": f"""
        SELECT
            HOUR(date_parse(substr(w.start_time,1,19), '%Y-%m-%d %H:%i:%s'))
                                                    AS hora_inicio,
            COUNT(*)                                AS sesiones,
            ROUND(AVG(s.sleep_score), 0)            AS score_medio,
            ROUND(AVG(s.hrv_avg), 0)                AS hrv_medio,
            ROUND(AVG(s.total_sleep_seconds)/3600,1) AS horas_sueno,
            ROUND(AVG(s.deep_sleep_seconds)/3600, 1) AS profundo_h
        FROM workouts w
        {JOIN_CONDITION}
        GROUP BY HOUR(date_parse(substr(w.start_time,1,19), '%Y-%m-%d %H:%i:%s'))
        ORDER BY hora_inicio
    """,

    "Tiempo fin entrenamiento -> dormir vs calidad sueno": f"""
        SELECT
            CASE
                WHEN date_diff('minute',
                        date_add('second', CAST(w.duration_seconds AS INTEGER),
                            date_parse(substr(w.start_time,1,19), '%Y-%m-%d %H:%i:%s')),
                        date_parse(substr(s.sleep_start,1,19), '%Y-%m-%dT%H:%i:%s')
                     ) < 120 THEN 'menos de 2h'
                WHEN date_diff('minute',
                        date_add('second', CAST(w.duration_seconds AS INTEGER),
                            date_parse(substr(w.start_time,1,19), '%Y-%m-%d %H:%i:%s')),
                        date_parse(substr(s.sleep_start,1,19), '%Y-%m-%dT%H:%i:%s')
                     ) < 180 THEN '2h - 3h'
                ELSE 'mas de 3h'
            END                                     AS ventana,
            COUNT(*)                                AS sesiones,
            ROUND(AVG(s.sleep_score), 0)            AS score_medio,
            ROUND(AVG(s.hrv_avg), 0)                AS hrv_medio,
            ROUND(AVG(s.total_sleep_seconds)/3600,1) AS horas_sueno
        FROM workouts w
        {JOIN_CONDITION}
        GROUP BY 1
        ORDER BY MIN(date_diff('minute',
            date_add('second', CAST(w.duration_seconds AS INTEGER),
                date_parse(substr(w.start_time,1,19), '%Y-%m-%d %H:%i:%s')),
            date_parse(substr(s.sleep_start,1,19), '%Y-%m-%dT%H:%i:%s')
        ))
    """,

    "Todas las zonas por sesion vs sueno": f"""
        SELECT
            w.workout_date                                              AS fecha,
            w.type                                                      AS tipo,
            CAST(w.max_hr AS INTEGER)                                  AS fc_max,
            CAST(COALESCE(w.zone1_seconds,0)/60 AS INTEGER)           AS z1_min,
            CAST(COALESCE(w.zone2_seconds,0)/60 AS INTEGER)           AS z2_min,
            CAST(COALESCE(w.zone3_seconds,0)/60 AS INTEGER)           AS z3_min,
            CAST(COALESCE(w.zone4_seconds,0)/60 AS INTEGER)           AS z4_min,
            CAST(COALESCE(w.zone5_seconds,0)/60 AS INTEGER)           AS z5_min,
            CAST(s.sleep_score AS INTEGER)                             AS score_sueno,
            CAST(s.hrv_avg AS INTEGER)                                 AS hrv,
            s.hrv_status                                               AS hrv_estado,
            ROUND(s.deep_sleep_seconds/3600.0, 1)                     AS profundo_h,
            ROUND(s.rem_sleep_seconds/3600.0, 1)                      AS rem_h
        FROM workouts w
        {JOIN_CONDITION}
        ORDER BY w.workout_date DESC
    """,

    "Zona dominante vs calidad del sueno": f"""
        SELECT
            CASE
                WHEN COALESCE(w.zone5_seconds,0) > 600  THEN 'Z5 max (>10min picos)'
                WHEN COALESCE(w.zone4_seconds,0) > 1200 THEN 'Z4 umbral (>20min)'
                WHEN COALESCE(w.zone3_seconds,0) > 1800 THEN 'Z3 tempo (>30min)'
                WHEN COALESCE(w.zone2_seconds,0) > 2400 THEN 'Z2 aerobico (>40min)'
                ELSE                                         'Z1 recuperacion'
            END                                             AS zona_dominante,
            COUNT(*)                                        AS sesiones,
            ROUND(AVG(COALESCE(w.zone4_seconds,0)
                    + COALESCE(w.zone5_seconds,0))/60, 0)  AS min_alta_intensidad,
            ROUND(AVG(s.sleep_score), 0)                   AS score_sueno,
            ROUND(AVG(s.hrv_avg), 0)                       AS hrv_medio,
            ROUND(AVG(s.total_sleep_seconds)/3600, 1)      AS horas_sueno,
            ROUND(AVG(s.deep_sleep_seconds)/3600, 1)       AS profundo_h,
            ROUND(AVG(s.rem_sleep_seconds)/3600, 1)        AS rem_h
        FROM workouts w
        {JOIN_CONDITION}
        GROUP BY 1
        ORDER BY MIN(COALESCE(w.zone5_seconds,0) + COALESCE(w.zone4_seconds,0)) DESC
    """,

    "Bici (steady) vs running/pista (intervals) -> sueno": f"""
        SELECT
            CASE
                WHEN w.type = 'road_biking' THEN 'Bici (steady)'
                WHEN w.type IN ('track_running','running') THEN 'Running/Pista (intervals)'
                ELSE w.type
            END                                             AS categoria,
            COUNT(*)                                        AS sesiones,
            ROUND(AVG(w.max_hr), 0)                        AS fc_max_media,
            ROUND(AVG(w.anaerobic_effect), 1)              AS efecto_anaerobico,
            ROUND(AVG(COALESCE(w.zone5_seconds,0)/60), 0) AS min_zona5_media,
            ROUND(AVG(s.sleep_score), 0)                   AS score_sueno,
            ROUND(AVG(s.hrv_avg), 0)                       AS hrv_medio,
            ROUND(AVG(s.total_sleep_seconds)/3600, 1)      AS horas_sueno
        FROM workouts w
        {JOIN_CONDITION}
        WHERE w.type IN ('road_biking','track_running','running')
        GROUP BY 1
        ORDER BY 1
    """,
}


def run_query(sql: str) -> list[dict]:
    response = _athena.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={"Database": config.ATHENA_DATABASE},
        ResultConfiguration={"OutputLocation": config.ATHENA_RESULTS_PREFIX},
    )
    execution_id = response["QueryExecutionId"]
    while True:
        status = _athena.get_query_execution(QueryExecutionId=execution_id)
        state = status["QueryExecution"]["Status"]["State"]
        if state in ("SUCCEEDED", "FAILED", "CANCELLED"):
            break
        time.sleep(1)
    if state != "SUCCEEDED":
        reason = status["QueryExecution"]["Status"].get("StateChangeReason", "")
        raise RuntimeError(f"Query fallida ({state}): {reason}")
    results = _athena.get_query_results(QueryExecutionId=execution_id)
    rows = results["ResultSet"]["Rows"]
    headers = [c["VarCharValue"] for c in rows[0]["Data"]]
    return [
        {headers[i]: col.get("VarCharValue", "") for i, col in enumerate(row["Data"])}
        for row in rows[1:]
    ]


def print_table(title: str, rows: list[dict]) -> None:
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")
    if not rows:
        print("  (sin datos suficientes)")
        return
    headers = list(rows[0].keys())
    col_widths = {h: max(len(h), max((len(r.get(h) or "") for r in rows))) for h in headers}
    header_line = "  " + "  ".join(h.ljust(col_widths[h]) for h in headers)
    print(header_line)
    print("  " + "-" * (len(header_line) - 2))
    for row in rows:
        print("  " + "  ".join((row.get(h) or "").ljust(col_widths[h]) for h in headers))


if __name__ == "__main__":
    print("Analizando impacto del entrenamiento en el sueno...\n")
    for title, sql in QUERIES.items():
        try:
            rows = run_query(sql)
            print_table(title, rows)
        except Exception as e:
            print(f"\n[ERROR] {title}: {e}")
    print(f"\n{'=' * 70}")
    print("  NOTA: sleep_date en Garmin = dia en que te despiertas.")
    print("  Cada fila une el entrenamiento del dia N con el sueno de la noche N->N+1.")
    print(f"{'=' * 70}")
