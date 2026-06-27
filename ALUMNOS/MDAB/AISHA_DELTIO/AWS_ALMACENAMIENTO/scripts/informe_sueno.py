"""
Informe personalizado: como tus entrenamientos afectan al sueno.
Combina datos de Athena y genera conclusiones y recomendaciones.
"""
import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import boto3
from src import config

_athena = boto3.client("athena", region_name=config.AWS_REGION)

QUERY = """
    SELECT
        w.workout_date,
        w.type,
        w.name,
        HOUR(date_parse(substr(w.start_time,1,19), '%Y-%m-%d %H:%i:%s'))   AS hora_inicio,
        ROUND(w.duration_seconds / 60)                                       AS duracion_min,
        CAST(w.avg_hr  AS INTEGER)                                           AS avg_hr,
        CAST(w.max_hr  AS INTEGER)                                           AS max_hr,
        ROUND(w.anaerobic_effect, 1)                                         AS anaerobic_effect,
        CAST(COALESCE(w.zone1_seconds,0) / 60 AS INTEGER)                   AS z1,
        CAST(COALESCE(w.zone2_seconds,0) / 60 AS INTEGER)                   AS z2,
        CAST(COALESCE(w.zone3_seconds,0) / 60 AS INTEGER)                   AS z3,
        CAST(COALESCE(w.zone4_seconds,0) / 60 AS INTEGER)                   AS z4,
        CAST(COALESCE(w.zone5_seconds,0) / 60 AS INTEGER)                   AS z5,
        ROUND(w.temp_c, 1)                                                   AS temp_c,
        ROUND(w.feels_like_c, 1)                                             AS feels_like_c,
        CAST(w.humidity_pct AS INTEGER)                                      AS humidity_pct,
        ROUND(w.precipitation_mm, 1)                                         AS precipitation_mm,
        ROUND(w.wind_speed_kmh, 1)                                           AS wind_speed_kmh,
        date_diff('minute',
            date_add('second', CAST(w.duration_seconds AS INTEGER),
                date_parse(substr(w.start_time,1,19), '%Y-%m-%d %H:%i:%s')),
            date_parse(substr(s.sleep_start,1,19), '%Y-%m-%dT%H:%i:%s')
        )                                                                    AS min_fin_a_dormir,
        CAST(s.sleep_score AS INTEGER)                                       AS sleep_score,
        ROUND(s.total_sleep_seconds / 3600.0, 1)                            AS horas_sueno,
        ROUND(s.deep_sleep_seconds  / 3600.0, 1)                            AS profundo_h,
        ROUND(s.rem_sleep_seconds   / 3600.0, 1)                            AS rem_h,
        CAST(s.hrv_avg AS INTEGER)                                           AS hrv,
        s.hrv_status
    FROM workouts w
    JOIN sleep s
      ON s.sleep_date = date_format(
            date_add('day', 1, date_parse(w.workout_date, '%Y-%m-%d')),
            '%Y-%m-%d'
         )
    ORDER BY w.workout_date DESC
"""


# ─── helpers ─────────────────────────────────────────────────────────────────

def run_query(sql: str) -> list[dict]:
    resp = _athena.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={"Database": config.ATHENA_DATABASE},
        ResultConfiguration={"OutputLocation": config.ATHENA_RESULTS_PREFIX},
    )
    eid = resp["QueryExecutionId"]
    while True:
        st = _athena.get_query_execution(QueryExecutionId=eid)["QueryExecution"]["Status"]["State"]
        if st in ("SUCCEEDED", "FAILED", "CANCELLED"):
            break
        time.sleep(1)
    if st != "SUCCEEDED":
        raise RuntimeError(f"Query fallida: {st}")
    rows = _athena.get_query_results(QueryExecutionId=eid)["ResultSet"]["Rows"]
    headers = [c["VarCharValue"] for c in rows[0]["Data"]]
    return [{headers[i]: col.get("VarCharValue") for i, col in enumerate(r["Data"])} for r in rows[1:]]


def f(val, decimals=1):
    """Float seguro desde string."""
    try:
        return round(float(val), decimals) if val else None
    except (ValueError, TypeError):
        return None


def i(val):
    """Int seguro desde string."""
    try:
        return int(val) if val else None
    except (ValueError, TypeError):
        return None


def avg(values):
    vals = [v for v in values if v is not None]
    return round(sum(vals) / len(vals), 1) if vals else None


def regression(xs, ys):
    """Regresion lineal simple. Devuelve (pendiente, intercepto)."""
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 3:
        return None, None
    n = len(pairs)
    mx = sum(p[0] for p in pairs) / n
    my = sum(p[1] for p in pairs) / n
    ssxy = sum((p[0]-mx)*(p[1]-my) for p in pairs)
    ssxx = sum((p[0]-mx)**2 for p in pairs)
    if ssxx == 0:
        return None, None
    slope = ssxy / ssxx
    return round(slope, 2), round(my - slope * mx, 1)


def zone_label(row):
    if row["z5"] > 10:
        return "Z5-max  (picos altos >10min)"
    elif row["z4"] > 20:
        return "Z4-umbral (series >20min)"
    elif row["z3"] > 30:
        return "Z3-tempo  (>30min)"
    elif row["z2"] > 40:
        return "Z2-aerob  (>40min)"
    else:
        return "Z1-recup  (suave)"


def hour_bucket(h):
    if h is None:
        return "desconocida"
    if h < 13:
        return f"manana  ({h:02d}h)"
    elif h < 17:
        return f"tarde   ({h:02d}h)"
    elif h < 19:
        return f"noche-t ({h:02d}h)"
    else:
        return f"noche   ({h:02d}h)"


def type_label(t):
    if t == "road_biking":
        return "Bici (steady)"
    elif t in ("track_running", "running"):
        return "Running/Pista (intervals)"
    elif t == "walking":
        return "Paseo"
    return t or "otro"


def sep(char="=", n=65):
    print(char * n)


def section(title):
    print()
    sep()
    print(f"  {title}")
    sep()


def table(rows_dict, cols):
    """Imprime lista de dicts como tabla simple."""
    if not rows_dict:
        print("  (sin datos)")
        return
    widths = {c: max(len(c), max(len(str(r.get(c, ""))) for r in rows_dict)) for c in cols}
    header = "  " + "  ".join(c.ljust(widths[c]) for c in cols)
    print(header)
    print("  " + "-" * (len(header) - 2))
    for r in rows_dict:
        print("  " + "  ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))


# ─── análisis ────────────────────────────────────────────────────────────────

def cast_row(row):
    return {
        **row,
        "hora_inicio":      i(row["hora_inicio"]),
        "duracion_min":     f(row["duracion_min"], 0),
        "avg_hr":           i(row["avg_hr"]),
        "max_hr":           i(row["max_hr"]),
        "anaerobic_effect": f(row["anaerobic_effect"]),
        "z1": i(row["z1"]), "z2": i(row["z2"]), "z3": i(row["z3"]),
        "z4": i(row["z4"]), "z5": i(row["z5"]),
        "temp_c":           f(row.get("temp_c")),
        "feels_like_c":     f(row.get("feels_like_c")),
        "humidity_pct":     i(row.get("humidity_pct")),
        "precipitation_mm": f(row.get("precipitation_mm")),
        "wind_speed_kmh":   f(row.get("wind_speed_kmh")),
        "min_fin_a_dormir": i(row["min_fin_a_dormir"]),
        "sleep_score":      i(row["sleep_score"]),
        "horas_sueno":      f(row["horas_sueno"]),
        "profundo_h":       f(row["profundo_h"]),
        "rem_h":            f(row["rem_h"]),
        "hrv":              i(row["hrv"]),
    }


def group_avg(rows, key_fn, metrics):
    groups = {}
    for r in rows:
        k = key_fn(r)
        groups.setdefault(k, []).append(r)
    result = []
    for k, rs in sorted(groups.items()):
        entry = {"grupo": k, "n": len(rs)}
        for m in metrics:
            entry[m] = avg([r[m] for r in rs])
        result.append(entry)
    return result


def main():
    print("Obteniendo datos de Athena...")
    raw = run_query(QUERY)
    data = [cast_row(r) for r in raw]
    n = len(data)

    # ── 0. Cabecera ──────────────────────────────────────────────────────────
    print()
    sep("=")
    print("  INFORME: IMPACTO DEL ENTRENAMIENTO EN EL SUENO")
    print(f"  {n} sesiones analizadas (ultimos 60 dias)")
    sep("=")

    # ── 1. Resumen global ────────────────────────────────────────────────────
    section("1. RESUMEN GLOBAL")
    score_global = avg([r["sleep_score"] for r in data])
    horas_global = avg([r["horas_sueno"] for r in data])
    hrv_global   = avg([r["hrv"] for r in data])
    print(f"  Score sueno medio  : {score_global}")
    print(f"  Horas sueno media  : {horas_global}h")
    print(f"  HRV medio          : {hrv_global}")

    # ── 2. Zona dominante ────────────────────────────────────────────────────
    section("2. ZONA DOMINANTE vs SUENO")
    print("  (clasificacion por zona que mas tiempo acumulas en cada sesion)\n")
    by_zone = group_avg(data, zone_label, ["sleep_score", "horas_sueno", "hrv", "profundo_h", "rem_h"])
    for r in sorted(by_zone, key=lambda x: -(x["sleep_score"] or 0)):
        print(f"  {r['grupo']:<30}  n={r['n']}  score={r['sleep_score']}  "
              f"hrv={r['hrv']}  {r['horas_sueno']}h  profundo:{r['profundo_h']}h  REM:{r['rem_h']}h")

    # ── 3. Impacto cuantificado de la zona 5 ─────────────────────────────────
    section("3. CADA MINUTO EN ZONA 5 TE CUESTA...")
    slope, intercept = regression([r["z5"] for r in data], [r["sleep_score"] for r in data])
    slope_h, _ = regression([r["z5"] for r in data], [r["horas_sueno"] for r in data])
    slope_hrv, _ = regression([r["z5"] for r in data], [r["hrv"] for r in data])
    if slope:
        print(f"  Score sueno  : {slope:+.2f} puntos por minuto en Z5")
        print(f"  Horas sueno  : {slope_h:+.2f} horas por minuto en Z5")
        print(f"  HRV          : {slope_hrv:+.2f} puntos por minuto en Z5")
        print()
        for umbral in [5, 10, 15, 20]:
            pred_score = round(intercept + slope * umbral, 0)
            pred_h = round((_ or 0) + (slope_h or 0) * umbral, 1) if slope_h else "?"
            print(f"  Con {umbral:>2} min en Z5 -> score estimado: {pred_score}")

    # ── 4. Tipo de entrenamiento ─────────────────────────────────────────────
    section("4. TIPO DE ENTRENAMIENTO vs SUENO")
    by_type = group_avg(data, lambda r: type_label(r["type"]),
                        ["sleep_score", "horas_sueno", "hrv", "max_hr", "z4", "z5", "profundo_h", "rem_h"])
    for r in sorted(by_type, key=lambda x: -(x["sleep_score"] or 0)):
        print(f"  {r['grupo']:<25}  n={r['n']}  score={r['sleep_score']}  "
              f"hrv={r['hrv']}  {r['horas_sueno']}h  "
              f"z4={r['z4']}min  z5={r['z5']}min")

    # ── 5. Hora del entrenamiento ─────────────────────────────────────────────
    section("5. HORA DEL ENTRENAMIENTO vs SUENO")
    by_hour = group_avg(data, lambda r: hour_bucket(r["hora_inicio"]),
                        ["sleep_score", "horas_sueno", "hrv", "min_fin_a_dormir"])
    print(f"  {'Franja':<20}  {'n':>3}  {'score':>6}  {'hrv':>5}  {'horas':>6}  {'min fin->dormir':>16}")
    sep("-", 65)
    for r in sorted(by_hour, key=lambda x: x["grupo"]):
        print(f"  {r['grupo']:<20}  {r['n']:>3}  {str(r['sleep_score']):>6}  "
              f"{str(r['hrv']):>5}  {str(r['horas_sueno']):>6}  {str(r['min_fin_a_dormir']):>16}")

    # ── 6. Hora + intensidad combinadas ──────────────────────────────────────
    section("6. HORA + INTENSIDAD (Z5) - DETALLE")
    print(f"  {'Hora':>5}  {'Tipo':<22}  {'z5':>4}  {'score':>6}  {'hrv':>5}  {'horas':>6}  {'min->dormir':>12}")
    sep("-", 65)
    for r in sorted(data, key=lambda x: (x["hora_inicio"] or 0, -(x["z5"] or 0))):
        print(f"  {str(r['hora_inicio'] or '?'):>5}h  {type_label(r['type']):<22}  "
              f"{str(r['z5'] or 0):>4}  {str(r['sleep_score'] or '?'):>6}  "
              f"{str(r['hrv'] or '?'):>5}  {str(r['horas_sueno'] or '?'):>6}  "
              f"{str(r['min_fin_a_dormir'] or '?'):>12}")

    # ── 7. Tiempo entre fin del entreno y dormir ──────────────────────────────
    section("7. TIEMPO FIN ENTRENO -> DORMIR")
    buckets = {"<2h": [], "2-3h": [], "3-4h": [], ">4h": []}
    for r in data:
        m = r["min_fin_a_dormir"]
        if m is None:
            continue
        if m < 120:
            buckets["<2h"].append(r)
        elif m < 180:
            buckets["2-3h"].append(r)
        elif m < 240:
            buckets["3-4h"].append(r)
        else:
            buckets[">4h"].append(r)
    for k, rs in buckets.items():
        if rs:
            print(f"  {k:<6}  n={len(rs)}  score={avg([r['sleep_score'] for r in rs])}  "
                  f"hrv={avg([r['hrv'] for r in rs])}  {avg([r['horas_sueno'] for r in rs])}h")

    # ── 8. Tus mejores y peores noches despues de entrenar ───────────────────
    section("8. TUS MEJORES NOCHES TRAS ENTRENAR (top 5)")
    top5 = sorted(data, key=lambda r: r["sleep_score"] or 0, reverse=True)[:5]
    for r in top5:
        print(f"  {r['workout_date']}  {type_label(r['type']):<25}  "
              f"z4={r['z4']}min z5={r['z5']}min  hora={r['hora_inicio']}h  "
              f"-> score={r['sleep_score']}  hrv={r['hrv']}")

    section("9. TUS PEORES NOCHES TRAS ENTRENAR (top 5)")
    bot5 = sorted(data, key=lambda r: r["sleep_score"] or 999)[:5]
    for r in bot5:
        print(f"  {r['workout_date']}  {type_label(r['type']):<25}  "
              f"z4={r['z4']}min z5={r['z5']}min  hora={r['hora_inicio']}h  "
              f"-> score={r['sleep_score']}  hrv={r['hrv']}")

    # ── 9. Recomendaciones ───────────────────────────────────────────────────
    # ── temperatura ──────────────────────────────────────────────────────────
    section("10. TEMPERATURA AL ENTRENAR vs SUENO")

    def temp_bucket(row):
        t = row.get("temp_c")
        if t is None:
            return "sin datos"
        if t < 18:
            return "fresco  (<18C)"
        elif t < 25:
            return "templado (18-25C)"
        elif t < 30:
            return "calor   (25-30C)"
        else:
            return "mucho calor (>30C)"

    by_temp = group_avg(data, temp_bucket, ["sleep_score", "horas_sueno", "hrv", "z5"])
    print(f"  {'Temperatura':<22}  {'n':>3}  {'score':>6}  {'hrv':>5}  {'horas':>6}  {'z5_min':>7}")
    sep("-", 65)
    for r in sorted(by_temp, key=lambda x: x["grupo"]):
        print(f"  {r['grupo']:<22}  {r['n']:>3}  {str(r['sleep_score']):>6}  "
              f"{str(r['hrv']):>5}  {str(r['horas_sueno']):>6}  {str(r['z5']):>7}")

    # temperatura + z5 combinados
    print()
    slope_t, intercept_t = regression(
        [r["temp_c"] for r in data], [r["sleep_score"] for r in data]
    )
    slope_t_hrv, _ = regression(
        [r["temp_c"] for r in data], [r["hrv"] for r in data]
    )
    if slope_t:
        print(f"  Por cada grado mas de temperatura al entrenar:")
        print(f"    Score sueno  : {slope_t:+.2f} puntos")
        print(f"    HRV          : {slope_t_hrv:+.2f} puntos")

    # calor + alta intensidad (la combinacion mas dura)
    calor_z5 = [r for r in data if (r.get("temp_c") or 0) >= 25 and (r["z5"] or 0) > 5]
    fresco_z5 = [r for r in data if (r.get("temp_c") or 100) < 22 and (r["z5"] or 0) > 5]
    if calor_z5 and fresco_z5:
        print(f"\n  Series (Z5>5min) con calor (>25C): score={avg([r['sleep_score'] for r in calor_z5])}  "
              f"hrv={avg([r['hrv'] for r in calor_z5])}  n={len(calor_z5)}")
        print(f"  Series (Z5>5min) con fresco (<22C): score={avg([r['sleep_score'] for r in fresco_z5])}  "
              f"hrv={avg([r['hrv'] for r in fresco_z5])}  n={len(fresco_z5)}")

    section("11. RECOMENDACIONES PERSONALIZADAS")

    # Calcular umbrales desde los datos
    high_z5 = [r for r in data if (r["z5"] or 0) > 10]
    low_z5  = [r for r in data if (r["z5"] or 0) <= 5]
    late    = [r for r in data if (r["hora_inicio"] or 0) >= 19]
    early   = [r for r in data if (r["hora_inicio"] or 0) < 18]
    biking  = [r for r in data if r["type"] == "road_biking"]
    running = [r for r in data if r["type"] in ("track_running", "running")]

    score_high_z5  = avg([r["sleep_score"] for r in high_z5])
    score_low_z5   = avg([r["sleep_score"] for r in low_z5])
    score_late     = avg([r["sleep_score"] for r in late])
    score_early    = avg([r["sleep_score"] for r in early])
    score_biking   = avg([r["sleep_score"] for r in biking])
    score_running  = avg([r["sleep_score"] for r in running])
    hrv_biking     = avg([r["hrv"] for r in biking])
    hrv_running    = avg([r["hrv"] for r in running])

    rec = []

    diff_z5 = round((score_high_z5 or 0) - (score_low_z5 or 0), 0) if score_high_z5 and score_low_z5 else 0
    if diff_z5 < -3:
        rec.append(
            f"[INTENSIDAD] Cuando superas 10 min en Z5 duermes {abs(diff_z5)} puntos peor (score "
            f"{score_high_z5} vs {score_low_z5}). Intenta que tus series tengan pausas largas "
            f"para bajar FC antes de acumular mas tiempo en Z5."
        )

    diff_hora = round((score_late or 0) - (score_early or 0), 0) if score_late and score_early else 0
    if diff_hora < -3:
        rec.append(
            f"[HORA] Entrenar a las 19h+ da un score {abs(diff_hora)} puntos peor que antes "
            f"de las 18h ({score_late} vs {score_early}). Si puedes adelantar la sesion de pista "
            f"a las 18h, ganas en calidad de sueno."
        )
    elif score_early and score_late:
        rec.append(
            f"[HORA] La hora del entreno no te afecta mucho (18h: {score_early} vs 19h+: {score_late}). "
            f"Pero la sesion termina mas tarde, lo que reduce el margen antes de dormir."
        )

    if score_biking and score_running:
        diff_tipo = round(score_biking - score_running, 0)
        if diff_tipo > 2:
            rec.append(
                f"[TIPO] La bici te da {diff_tipo} puntos mas de score que pista/running "
                f"({score_biking} vs {score_running}) y HRV {hrv_biking} vs {hrv_running}. "
                f"La vispera de una serie importante, considera bici suave en lugar de otro running."
            )

    if slope:
        rec.append(
            f"[Z5 CUANTIFICADO] Por cada minuto extra en Z5 pierdes ~{abs(slope):.1f} pts de score "
            f"y ~{abs(slope_h or 0):.2f}h de sueno. Tu 'punto dulce' es <10 min en Z5 con buenas pausas."
        )

    rec.append(
        "[MEJOR PATRON] Tus mejores noches tras entrenar tienen en comun: Z5 < 5 min, sesion "
        "terminada antes de las 21h, y tipo bici o series cortas (4x300, 2x5x300 con poca Z5)."
    )
    rec.append(
        "[RECUPERACION] Despues de sesiones con HRV bajo (Z5 alto), prioriza bici Z2 o descanso "
        "al dia siguiente. Acumular sesiones duras seguidas baja tu HRV de forma sostenida."
    )

    if slope_t and slope_t < -0.2:
        rec.append(
            f"[TEMPERATURA] Por cada grado mas al entrenar pierdes ~{abs(slope_t):.2f} pts de score. "
            f"En dias de calor (>28C) con series de pista, considera salir mas temprano (antes de las 19h) "
            f"o reducir el volumen en Z5 para compensar el estres termico extra."
        )
    elif slope_t:
        rec.append(
            f"[TEMPERATURA] La temperatura tiene un impacto moderado ({slope_t:+.2f} pts/grado). "
            f"La combinacion de calor + alta intensidad (Z5) es la mas perjudicial para el sueno."
        )

    for idx, r in enumerate(rec, 1):
        print(f"\n  {idx}. {r}")

    sep()
    print()


if __name__ == "__main__":
    main()
