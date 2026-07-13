"""
Genera un informe PDF visual: Como tus entrenamientos afectan al sueno.
Uso  : python scripts/generar_pdf.py
Salida: informe_garmin_YYYYMMDD.pdf
"""
import sys
import os
import time
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch
import numpy as np

import boto3
from src import config

# ── Paleta ────────────────────────────────────────────────────────────────────
C = {
    "navy":   "#0f2d5e",
    "blue":   "#1d4ed8",
    "sky":    "#3b82f6",
    "light":  "#dbeafe",
    "green":  "#16a34a",
    "lgreen": "#dcfce7",
    "amber":  "#d97706",
    "lamber": "#fef3c7",
    "red":    "#dc2626",
    "lred":   "#fee2e2",
    "gray":   "#64748b",
    "lgray":  "#f8fafc",
    "text":   "#1e293b",
    "white":  "#ffffff",
}

A4 = (8.27, 11.69)

plt.rcParams.update({
    "font.family":        "DejaVu Sans",
    "font.size":          10,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.titlesize":     12,
    "axes.titleweight":   "bold",
    "figure.dpi":         150,
})

# ── Athena ────────────────────────────────────────────────────────────────────
_athena = boto3.client("athena", region_name=config.AWS_REGION)

QUERY_SESSIONS = """
    SELECT
        w.workout_date,
        w.type,
        w.name,
        HOUR(date_parse(substr(w.start_time,1,19), '%Y-%m-%d %H:%i:%s')) AS hora,
        CAST(w.avg_hr  AS INTEGER)                                        AS avg_hr,
        CAST(w.max_hr  AS INTEGER)                                        AS max_hr,
        ROUND(w.anaerobic_effect, 1)                                      AS anaerobic,
        CAST(COALESCE(w.zone1_seconds,0)/60 AS INTEGER)                  AS z1,
        CAST(COALESCE(w.zone2_seconds,0)/60 AS INTEGER)                  AS z2,
        CAST(COALESCE(w.zone3_seconds,0)/60 AS INTEGER)                  AS z3,
        CAST(COALESCE(w.zone4_seconds,0)/60 AS INTEGER)                  AS z4,
        CAST(COALESCE(w.zone5_seconds,0)/60 AS INTEGER)                  AS z5,
        ROUND(w.temp_c, 1)                                               AS temp_c,
        CAST(w.body_battery_start AS INTEGER)                            AS bb_start,
        CAST(w.body_battery_drop  AS INTEGER)                            AS bb_drop,
        CAST(w.training_readiness AS INTEGER)                            AS training_readiness,
        CAST(w.stress_avg         AS INTEGER)                            AS stress_avg,
        date_diff('minute',
            date_add('second', CAST(w.duration_seconds AS INTEGER),
                date_parse(substr(w.start_time,1,19), '%Y-%m-%d %H:%i:%s')),
            date_parse(substr(s.sleep_start,1,19), '%Y-%m-%dT%H:%i:%s')
        )                                                                 AS min_fin_dormir,
        CAST(s.sleep_score AS INTEGER)                                    AS score,
        ROUND(s.total_sleep_seconds/3600.0, 1)                           AS horas,
        ROUND(s.deep_sleep_seconds/3600.0, 1)                            AS profundo,
        ROUND(s.rem_sleep_seconds/3600.0, 1)                             AS rem,
        CAST(s.hrv_avg AS INTEGER)                                        AS hrv,
        s.hrv_status
    FROM workouts w
    JOIN sleep s
      ON s.sleep_date = date_format(
            date_add('day', 1, date_parse(w.workout_date, '%Y-%m-%d')), '%Y-%m-%d')
    ORDER BY w.workout_date
"""

QUERY_SESSIONS_BASIC = """
    SELECT
        w.workout_date,
        w.type,
        w.name,
        HOUR(date_parse(substr(w.start_time,1,19), '%Y-%m-%d %H:%i:%s')) AS hora,
        CAST(w.avg_hr  AS INTEGER)                                        AS avg_hr,
        CAST(w.max_hr  AS INTEGER)                                        AS max_hr,
        ROUND(w.anaerobic_effect, 1)                                      AS anaerobic,
        CAST(COALESCE(w.zone1_seconds,0)/60 AS INTEGER)                  AS z1,
        CAST(COALESCE(w.zone2_seconds,0)/60 AS INTEGER)                  AS z2,
        CAST(COALESCE(w.zone3_seconds,0)/60 AS INTEGER)                  AS z3,
        CAST(COALESCE(w.zone4_seconds,0)/60 AS INTEGER)                  AS z4,
        CAST(COALESCE(w.zone5_seconds,0)/60 AS INTEGER)                  AS z5,
        ROUND(w.temp_c, 1)                                               AS temp_c,
        date_diff('minute',
            date_add('second', CAST(w.duration_seconds AS INTEGER),
                date_parse(substr(w.start_time,1,19), '%Y-%m-%d %H:%i:%s')),
            date_parse(substr(s.sleep_start,1,19), '%Y-%m-%dT%H:%i:%s')
        )                                                                 AS min_fin_dormir,
        CAST(s.sleep_score AS INTEGER)                                    AS score,
        ROUND(s.total_sleep_seconds/3600.0, 1)                           AS horas,
        ROUND(s.deep_sleep_seconds/3600.0, 1)                            AS profundo,
        ROUND(s.rem_sleep_seconds/3600.0, 1)                             AS rem,
        CAST(s.hrv_avg AS INTEGER)                                        AS hrv,
        s.hrv_status
    FROM workouts w
    JOIN sleep s
      ON s.sleep_date = date_format(
            date_add('day', 1, date_parse(w.workout_date, '%Y-%m-%d')), '%Y-%m-%d')
    ORDER BY w.workout_date
"""

QUERY_HISTORY = """
    SELECT sleep_date,
           CAST(sleep_score AS INTEGER)         AS score,
           CAST(hrv_avg AS INTEGER)             AS hrv,
           ROUND(total_sleep_seconds/3600.0, 1) AS horas
    FROM sleep
    ORDER BY sleep_date
"""


def _run(sql):
    r = _athena.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={"Database": config.ATHENA_DATABASE},
        ResultConfiguration={"OutputLocation": config.ATHENA_RESULTS_PREFIX},
    )
    eid = r["QueryExecutionId"]
    while True:
        st = _athena.get_query_execution(QueryExecutionId=eid)["QueryExecution"]["Status"]["State"]
        if st in ("SUCCEEDED", "FAILED", "CANCELLED"):
            break
        time.sleep(1)
    if st != "SUCCEEDED":
        raise RuntimeError(f"Query fallida: {st}")
    rows = _athena.get_query_results(QueryExecutionId=eid)["ResultSet"]["Rows"]
    hdrs = [c["VarCharValue"] for c in rows[0]["Data"]]
    return [{hdrs[i]: col.get("VarCharValue") for i, col in enumerate(r["Data"])} for r in rows[1:]]


def _f(v, dec=1):
    try:
        return round(float(v), dec) if v else None
    except Exception:
        return None


def _i(v):
    try:
        return int(v) if v else None
    except Exception:
        return None


def cast(rows):
    result = []
    for r in rows:
        result.append({
            **r,
            "hora":      _i(r.get("hora")),
            "avg_hr":    _i(r.get("avg_hr")),
            "max_hr":    _i(r.get("max_hr")),
            "anaerobic": _f(r.get("anaerobic")),
            "z1": _i(r.get("z1")), "z2": _i(r.get("z2")),
            "z3": _i(r.get("z3")), "z4": _i(r.get("z4")),
            "z5": _i(r.get("z5")),
            "temp_c":      _f(r.get("temp_c")),
            "min_fin_dormir": _i(r.get("min_fin_dormir")),
            "score":   _i(r.get("score")),
            "horas":   _f(r.get("horas")),
            "profundo":_f(r.get("profundo")),
            "rem":     _f(r.get("rem")),
            "hrv":     _i(r.get("hrv")),
            "bb_start":           _i(r.get("bb_start")),
            "bb_drop":            _i(r.get("bb_drop")),
            "training_readiness": _i(r.get("training_readiness")),
            "stress_avg":         _i(r.get("stress_avg")),
        })
    return result


def avg(vals):
    v = [x for x in vals if x is not None]
    return round(sum(v) / len(v), 1) if v else 0


def score_color(s):
    if s is None:
        return C["gray"]
    if s >= 85:
        return C["green"]
    if s >= 75:
        return C["amber"]
    return C["red"]


def zone_label(r):
    z5, z4, z3, z2 = r["z5"] or 0, r["z4"] or 0, r["z3"] or 0, r["z2"] or 0
    if z5 > 10:
        return "Z5-Max (picos >10min)"
    if z4 > 20:
        return "Z4-Umbral (series >20min)"
    if z3 > 30:
        return "Z3-Tempo (>30min)"
    if z2 > 40:
        return "Z2-Aerobico (>40min)"
    return "Z1-Recuperacion"


def type_label(t):
    if t == "road_biking":
        return "Bici"
    if t in ("track_running", "running"):
        return "Pista/Running"
    return "Paseo"


def header(fig, title, page, total_pages):
    fig.add_axes([0, 0.955, 1, 0.045]).set_axis_off()
    fig.patches.append(FancyBboxPatch(
        (0, 0.955), 1, 0.045,
        boxstyle="square,pad=0", linewidth=0,
        facecolor=C["navy"], transform=fig.transFigure, zorder=0
    ))
    fig.text(0.03, 0.978, title, fontsize=11, fontweight="bold",
             color=C["white"], va="center", transform=fig.transFigure)
    fig.text(0.97, 0.978, f"Aisha del Tio  |  {page}/{total_pages}",
             fontsize=8, color="#93c5fd", va="center", ha="right",
             transform=fig.transFigure)


def footer(fig, fecha):
    fig.text(0.5, 0.012, f"Generado el {fecha}  |  Datos: Garmin Connect + Open-Meteo",
             ha="center", fontsize=7, color=C["gray"], transform=fig.transFigure)


# ── PAGINA 1: Portada ─────────────────────────────────────────────────────────
def page_portada(pdf, data, fecha):
    fig = plt.figure(figsize=A4)
    fig.patch.set_facecolor(C["navy"])

    # Franja superior decorativa
    fig.add_axes([0, 0.88, 1, 0.12]).set_axis_off()
    ax_deco = fig.add_axes([0, 0.88, 1, 0.12])
    ax_deco.set_facecolor(C["blue"])
    ax_deco.set_axis_off()

    fig.text(0.5, 0.92, "G A R M I N   T R A I N I N G   R E P O R T", ha="center", fontsize=9,
             color="#93c5fd", fontweight="bold", transform=fig.transFigure)
    fig.text(0.5, 0.76, "Sueno y Recuperacion", ha="center", fontsize=30,
             color=C["white"], fontweight="bold", transform=fig.transFigure)
    fig.text(0.5, 0.70, "Como tus entrenamientos afectan a tu descanso",
             ha="center", fontsize=13, color="#93c5fd", transform=fig.transFigure)
    fig.text(0.5, 0.63, "Aisha del Tio", ha="center", fontsize=18,
             color=C["white"], fontweight="bold", transform=fig.transFigure)
    fig.text(0.5, 0.59, fecha, ha="center", fontsize=11,
             color="#cbd5e1", transform=fig.transFigure)

    # KPIs
    kpis = [
        ("Score de Sueno",  f"{avg([r['score'] for r in data]):.0f}",  "/100"),
        ("HRV Medio",       f"{avg([r['hrv']   for r in data]):.0f}",  "ms"),
        ("Horas de Sueno",  f"{avg([r['horas'] for r in data]):.1f}",  "h/noche"),
    ]
    kpi_colors = [C["sky"], C["green"], C["amber"]]
    for idx, (label, val, unit) in enumerate(kpis):
        x = 0.15 + idx * 0.28
        # Caja
        fig.patches.append(FancyBboxPatch(
            (x - 0.09, 0.41), 0.18, 0.15,
            boxstyle="round,pad=0.01", linewidth=2,
            edgecolor=kpi_colors[idx], facecolor="#1e3a6e",
            transform=fig.transFigure
        ))
        fig.text(x, 0.54, val, ha="center", fontsize=28, fontweight="bold",
                 color=kpi_colors[idx], transform=fig.transFigure)
        fig.text(x, 0.49, unit, ha="center", fontsize=9,
                 color="#94a3b8", transform=fig.transFigure)
        fig.text(x, 0.44, label, ha="center", fontsize=8,
                 color=C["white"], transform=fig.transFigure)

    # Estadisticas del periodo
    n = len(data)
    types = {}
    for r in data:
        k = type_label(r["type"])
        types[k] = types.get(k, 0) + 1
    stats_txt = f"{n} sesiones analizadas  |  "
    stats_txt += "  ".join(f"{v} {k}" for k, v in types.items())
    fig.text(0.5, 0.36, stats_txt, ha="center", fontsize=9,
             color="#94a3b8", transform=fig.transFigure)

    # Linea decorativa
    ax_line = fig.add_axes([0.1, 0.334, 0.8, 0.002])
    ax_line.set_facecolor(C["blue"])
    ax_line.set_axis_off()

    fig.text(0.5, 0.08,
             "Este informe combina tus datos de Garmin Connect con datos\n"
             "meteorologicos de Valencia para identificar los patrones\n"
             "que mejor y peor afectan a la calidad de tu sueno.",
             ha="center", fontsize=10, color="#94a3b8",
             transform=fig.transFigure, linespacing=1.8)

    pdf.savefig(fig, bbox_inches="tight")
    plt.close()


# ── PAGINA 2: Zonas FC y Tipo ─────────────────────────────────────────────────
def page_zonas_tipo(pdf, data, fecha):
    fig = plt.figure(figsize=A4)
    fig.patch.set_facecolor(C["white"])
    header(fig, "ZONAS DE FRECUENCIA CARDIACA Y TIPO DE ENTRENAMIENTO", 2, 6)
    footer(fig, fecha)

    gs = gridspec.GridSpec(2, 2, figure=fig,
                           top=0.90, bottom=0.08, left=0.10, right=0.95,
                           hspace=0.45, wspace=0.35)

    # ── Grafico 1: Zona dominante vs Score ───────────────────────────────────
    zone_order = ["Z5-Max (picos >10min)", "Z4-Umbral (series >20min)",
                  "Z3-Tempo (>30min)", "Z2-Aerobico (>40min)", "Z1-Recuperacion"]
    groups = {}
    for r in data:
        k = zone_label(r)
        groups.setdefault(k, []).append(r)

    labels, scores, hrvs, horas_vals = [], [], [], []
    for z in zone_order:
        rs = groups.get(z, [])
        if rs:
            labels.append(z.split("(")[0].strip())
            scores.append(avg([r["score"] for r in rs]))
            hrvs.append(avg([r["hrv"] for r in rs]))
            horas_vals.append(avg([r["horas"] for r in rs]))

    ax1 = fig.add_subplot(gs[0, 0])
    bars = ax1.barh(labels, scores, color=[score_color(s) for s in scores],
                    edgecolor="white", linewidth=0.5)
    ax1.set_xlim(60, 100)
    ax1.set_title("Zona dominante vs Score de sueno")
    ax1.set_xlabel("Score de sueno (/100)")
    for bar, val in zip(bars, scores):
        ax1.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                 f"{val:.0f}", va="center", fontsize=9, fontweight="bold")
    ax1.axvline(avg([r["score"] for r in data]), color=C["gray"],
                linestyle="--", linewidth=1, alpha=0.6, label="Media")
    ax1.legend(fontsize=8)
    ax1.set_facecolor(C["lgray"])

    # ── Grafico 2: Zona dominante vs HRV ─────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    bars2 = ax2.barh(labels, hrvs, color=C["sky"], edgecolor="white", linewidth=0.5)
    ax2.set_xlim(50, 110)
    ax2.set_title("Zona dominante vs HRV")
    ax2.set_xlabel("HRV medio (ms)")
    for bar, val in zip(bars2, hrvs):
        ax2.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                 f"{val:.0f}", va="center", fontsize=9, fontweight="bold")
    ax2.set_facecolor(C["lgray"])

    # ── Grafico 3: Tipo de entrenamiento (score + hrv + horas) ───────────────
    type_groups = {}
    for r in data:
        k = type_label(r["type"])
        type_groups.setdefault(k, []).append(r)

    t_labels = list(type_groups.keys())
    t_scores  = [avg([r["score"] for r in type_groups[k]]) for k in t_labels]
    t_hrvs    = [avg([r["hrv"]   for r in type_groups[k]]) for k in t_labels]
    t_horas   = [avg([r["horas"] for r in type_groups[k]]) for k in t_labels]

    ax3 = fig.add_subplot(gs[1, :])
    x = np.arange(len(t_labels))
    w = 0.25
    b1 = ax3.bar(x - w, t_scores,  w, label="Score sueno", color=C["blue"],   alpha=0.85)
    b2 = ax3.bar(x,     t_hrvs,    w, label="HRV (ms)",    color=C["green"],  alpha=0.85)
    b3 = ax3.bar(x + w, [h*10 for h in t_horas], w,
                 label="Horas x10", color=C["amber"], alpha=0.85)

    def autolabel(bars, scale=1):
        for bar in bars:
            h = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2, h + 0.5,
                     f"{h/scale:.1f}" if scale != 1 else f"{h:.0f}",
                     ha="center", va="bottom", fontsize=8, fontweight="bold")

    autolabel(b1)
    autolabel(b2)
    autolabel(b3, scale=10)

    ax3.set_xticks(x)
    ax3.set_xticklabels(t_labels, fontsize=10)
    ax3.set_title("Tipo de entrenamiento: Score / HRV / Horas de sueno")
    ax3.set_ylabel("Valor")
    ax3.legend(fontsize=9)
    ax3.set_facecolor(C["lgray"])

    pdf.savefig(fig, bbox_inches="tight")
    plt.close()


# ── PAGINA 3: Hora y Temperatura ──────────────────────────────────────────────
def page_hora_temp(pdf, data, fecha):
    fig = plt.figure(figsize=A4)
    fig.patch.set_facecolor(C["white"])
    header(fig, "HORA DEL ENTRENAMIENTO Y TEMPERATURA", 3, 6)
    footer(fig, fecha)

    gs = gridspec.GridSpec(2, 2, figure=fig,
                           top=0.90, bottom=0.08, left=0.10, right=0.95,
                           hspace=0.45, wspace=0.35)

    # ── Hora vs Score ─────────────────────────────────────────────────────────
    hour_groups = {}
    for r in data:
        h = r["hora"]
        if h is not None:
            hour_groups.setdefault(h, []).append(r)

    h_sorted = sorted(hour_groups.keys())
    h_labels  = [f"{h}h" for h in h_sorted]
    h_scores  = [avg([r["score"] for r in hour_groups[h]]) for h in h_sorted]
    h_hrv     = [avg([r["hrv"]   for r in hour_groups[h]]) for h in h_sorted]
    h_n       = [len(hour_groups[h]) for h in h_sorted]

    ax1 = fig.add_subplot(gs[0, 0])
    bars = ax1.bar(h_labels, h_scores, color=[score_color(s) for s in h_scores],
                   edgecolor="white", linewidth=0.5)
    ax1.set_ylim(55, 100)
    ax1.set_title("Hora de inicio vs Score de sueno")
    ax1.set_xlabel("Hora del entrenamiento")
    ax1.set_ylabel("Score de sueno (/100)")
    for bar, val, n in zip(bars, h_scores, h_n):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                 f"{val:.0f}\n(n={n})", ha="center", va="bottom", fontsize=8)
    ax1.axhline(avg([r["score"] for r in data]), color=C["gray"],
                linestyle="--", linewidth=1, alpha=0.7)
    ax1.set_facecolor(C["lgray"])

    # ── Hora vs HRV ───────────────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.bar(h_labels, h_hrv, color=C["sky"], edgecolor="white", linewidth=0.5)
    ax2.set_ylim(50, 110)
    ax2.set_title("Hora de inicio vs HRV")
    ax2.set_xlabel("Hora del entrenamiento")
    ax2.set_ylabel("HRV (ms)")
    for i, (h, v) in enumerate(zip(h_labels, h_hrv)):
        ax2.text(i, v + 0.5, f"{v:.0f}", ha="center", va="bottom",
                 fontsize=9, fontweight="bold")
    ax2.axhline(avg([r["hrv"] for r in data]), color=C["gray"],
                linestyle="--", linewidth=1, alpha=0.7)
    ax2.set_facecolor(C["lgray"])

    # ── Temperatura vs Score (scatter) ────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    type_colors = {"Bici": C["sky"], "Pista/Running": C["red"], "Paseo": C["green"]}
    for r in data:
        t, s = r["temp_c"], r["score"]
        if t is not None and s is not None:
            col = type_colors.get(type_label(r["type"]), C["gray"])
            ax3.scatter(t, s, color=col, s=60, alpha=0.8, edgecolors="white", linewidth=0.5)

    # Linea de tendencia
    temps_v = [r["temp_c"] for r in data if r["temp_c"] and r["score"]]
    scores_v = [r["score"] for r in data if r["temp_c"] and r["score"]]
    if len(temps_v) > 2:
        z = np.polyfit(temps_v, scores_v, 1)
        p = np.poly1d(z)
        xs = np.linspace(min(temps_v), max(temps_v), 100)
        ax3.plot(xs, p(xs), color=C["navy"], linewidth=1.5, linestyle="--", alpha=0.7)

    handles = [plt.scatter([], [], color=v, label=k, s=50)
               for k, v in type_colors.items()]
    ax3.legend(handles=handles, fontsize=8)
    ax3.set_title("Temperatura al entrenar vs Score de sueno")
    ax3.set_xlabel("Temperatura (degC)")
    ax3.set_ylabel("Score de sueno (/100)")
    ax3.set_facecolor(C["lgray"])

    # ── Temperatura vs HRV por buckets ────────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])

    def tbucket(r):
        t = r["temp_c"]
        if t is None: return None
        if t < 18:    return "Fresco\n(<18C)"
        if t < 25:    return "Templado\n(18-25C)"
        if t < 30:    return "Calor\n(25-30C)"
        return "Mucho calor\n(>30C)"

    tb_groups = {}
    for r in data:
        k = tbucket(r)
        if k:
            tb_groups.setdefault(k, []).append(r)

    tb_order = ["Fresco\n(<18C)", "Templado\n(18-25C)", "Calor\n(25-30C)", "Mucho calor\n(>30C)"]
    tb_labels  = [k for k in tb_order if k in tb_groups]
    tb_scores  = [avg([r["score"] for r in tb_groups[k]]) for k in tb_labels]
    tb_colors  = [C["sky"], C["amber"], C["red"], "#7c2d12"][:len(tb_labels)]

    bars4 = ax4.bar(range(len(tb_labels)), tb_scores, color=tb_colors,
                    edgecolor="white", linewidth=0.5)
    ax4.set_xticks(range(len(tb_labels)))
    ax4.set_xticklabels(tb_labels, fontsize=8)
    ax4.set_ylim(60, 100)
    ax4.set_title("Temperatura vs Score (agrupado)")
    ax4.set_ylabel("Score de sueno (/100)")
    for bar, val in zip(bars4, tb_scores):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                 f"{val:.0f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax4.set_facecolor(C["lgray"])

    pdf.savefig(fig, bbox_inches="tight")
    plt.close()


# ── PAGINA 4: Historial ───────────────────────────────────────────────────────
def page_historial(pdf, data, history, fecha):
    fig = plt.figure(figsize=A4)
    fig.patch.set_facecolor(C["white"])
    header(fig, "HISTORIAL: SUENO Y RECUPERACION (60 DIAS)", 4, 6)
    footer(fig, fecha)

    gs = gridspec.GridSpec(2, 1, figure=fig,
                           top=0.90, bottom=0.08, left=0.09, right=0.96,
                           hspace=0.40)

    all_dates  = [r["sleep_date"]           for r in history]
    all_scores = [_i(r.get("score")) or 0   for r in history]
    all_hrv    = [_i(r.get("hrv"))   or 0   for r in history]

    workout_dates = {r["workout_date"] for r in data}
    w_idx  = [i for i, d in enumerate(all_dates) if d in workout_dates]
    w_scr  = [all_scores[i] for i in w_idx]
    w_hrv  = [all_hrv[i]    for i in w_idx]

    x = np.arange(len(all_dates))

    # ── Score de sueno ────────────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0])
    ax1.fill_between(x, all_scores, alpha=0.15, color=C["blue"])
    ax1.plot(x, all_scores, color=C["blue"], linewidth=1.5, label="Score diario")
    ax1.scatter(w_idx, w_scr, color=C["red"], s=40, zorder=5,
                label="Noche tras entreno", edgecolors="white", linewidth=0.5)
    ax1.axhline(avg([r["score"] for r in data]), color=C["gray"],
                linestyle="--", linewidth=1, alpha=0.6, label="Media entrenos")
    ax1.set_ylim(40, 100)
    ax1.set_xlim(-0.5, len(x) - 0.5)
    ax1.set_title("Score de sueno diario")
    ax1.set_ylabel("Score (/100)")
    ax1.set_xticks(x[::7])
    ax1.set_xticklabels([all_dates[i][5:] for i in range(0, len(x), 7)],
                        fontsize=7, rotation=30)
    ax1.legend(fontsize=8, loc="upper left")
    ax1.set_facecolor(C["lgray"])

    # Zonas coloreadas
    ax1.axhspan(85, 100, alpha=0.05, color=C["green"])
    ax1.axhspan(75,  85, alpha=0.05, color=C["amber"])
    ax1.axhspan(0,   75, alpha=0.05, color=C["red"])
    ax1.text(len(x)-1, 90, "Optimo",  ha="right", fontsize=7, color=C["green"], alpha=0.7)
    ax1.text(len(x)-1, 79, "Bueno",   ha="right", fontsize=7, color=C["amber"], alpha=0.7)
    ax1.text(len(x)-1, 67, "Mejorar", ha="right", fontsize=7, color=C["red"],   alpha=0.7)

    # ── HRV ───────────────────────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[1])
    ax2.fill_between(x, all_hrv, alpha=0.15, color=C["green"])
    ax2.plot(x, all_hrv, color=C["green"], linewidth=1.5, label="HRV diario")
    ax2.scatter(w_idx, w_hrv, color=C["red"], s=40, zorder=5,
                label="Noche tras entreno", edgecolors="white", linewidth=0.5)
    ax2.axhline(avg([r["hrv"] for r in data]), color=C["gray"],
                linestyle="--", linewidth=1, alpha=0.6, label="Media entrenos")
    ax2.set_ylim(30, 120)
    ax2.set_xlim(-0.5, len(x) - 0.5)
    ax2.set_title("HRV nocturno diario")
    ax2.set_ylabel("HRV (ms)")
    ax2.set_xticks(x[::7])
    ax2.set_xticklabels([all_dates[i][5:] for i in range(0, len(x), 7)],
                        fontsize=7, rotation=30)
    ax2.legend(fontsize=8, loc="upper left")
    ax2.set_facecolor(C["lgray"])

    pdf.savefig(fig, bbox_inches="tight")
    plt.close()


# ── PAGINA 5: Mejores/Peores + Recomendaciones ────────────────────────────────
def page_recs(pdf, data, fecha):
    fig = plt.figure(figsize=A4)
    fig.patch.set_facecolor(C["white"])
    header(fig, "MEJORES SESIONES Y RECOMENDACIONES PERSONALIZADAS", 6, 6)
    footer(fig, fecha)

    gs = gridspec.GridSpec(3, 2, figure=fig,
                           top=0.89, bottom=0.05, left=0.05, right=0.97,
                           hspace=0.5, wspace=0.25)

    # ── Top 3 mejores ─────────────────────────────────────────────────────────
    def mini_table(ax, rows, title, header_color, row_color):
        ax.set_facecolor(row_color)
        ax.set_title(title, fontsize=10, fontweight="bold", color=header_color, pad=6)
        ax.axis("off")
        cols = ["Fecha", "Tipo", "Z5", "Score", "HRV"]
        y_header = 0.88
        xs = [0.02, 0.22, 0.58, 0.72, 0.86]
        for xp, col in zip(xs, cols):
            ax.text(xp, y_header, col, fontsize=7.5, fontweight="bold",
                    color=header_color, transform=ax.transAxes)
        ax.axhline(y_header - 0.06, color=header_color, linewidth=0.8, alpha=0.4)
        for i, r in enumerate(rows):
            y = y_header - 0.18 - i * 0.22
            vals = [
                r["workout_date"][5:],
                type_label(r["type"])[:10],
                f"{r['z5'] or 0}min",
                str(r["score"]),
                str(r["hrv"] or "-"),
            ]
            for xp, val in zip(xs, vals):
                ax.text(xp, y, val, fontsize=7.5, transform=ax.transAxes, color=C["text"])

    best3  = sorted(data, key=lambda r: r["score"] or 0, reverse=True)[:3]
    worst3 = sorted(data, key=lambda r: r["score"] or 999)[:3]

    ax_best  = fig.add_subplot(gs[0, 0])
    ax_worst = fig.add_subplot(gs[0, 1])
    mini_table(ax_best,  best3,  "Top 3 mejores noches", C["green"], C["lgreen"])
    mini_table(ax_worst, worst3, "Top 3 peores noches",  C["red"],   C["lred"])

    # ── Grafico Z5 vs Score (relacion directa) ────────────────────────────────
    ax_z5 = fig.add_subplot(gs[1, :])
    z5_vals = [r["z5"] or 0 for r in data]
    sc_vals = [r["score"] or 0 for r in data]
    colors_scatter = [type_colors_map(type_label(r["type"])) for r in data]
    ax_z5.scatter(z5_vals, sc_vals, c=colors_scatter, s=60, alpha=0.8,
                  edgecolors="white", linewidth=0.5)

    if len(z5_vals) > 2:
        z = np.polyfit(z5_vals, sc_vals, 1)
        p = np.poly1d(z)
        xs = np.linspace(0, max(z5_vals), 100)
        ax_z5.plot(xs, p(xs), color=C["navy"], linewidth=2, linestyle="--",
                   label=f"Tendencia: {z[0]:+.1f} pts/min Z5")

    ax_z5.set_title("Minutos en Zona 5 vs Score de sueno esa noche")
    ax_z5.set_xlabel("Minutos en Zona 5 (esfuerzo maximo)")
    ax_z5.set_ylabel("Score de sueno (/100)")
    ax_z5.legend(fontsize=9)
    ax_z5.set_facecolor(C["lgray"])

    # ── Recomendaciones ───────────────────────────────────────────────────────
    ax_r = fig.add_subplot(gs[2, :])
    ax_r.axis("off")
    ax_r.set_facecolor(C["white"])

    # Calcular recomendaciones desde datos
    s_z5_high = avg([r["score"] for r in data if (r["z5"] or 0) > 10])
    s_z5_low  = avg([r["score"] for r in data if (r["z5"] or 0) <= 5])
    s_bici    = avg([r["score"] for r in data if r["type"] == "road_biking"])
    s_pista   = avg([r["score"] for r in data if r["type"] in ("track_running", "running")])

    z5_vals_num = [r["z5"] or 0 for r in data]
    sc_vals_num = [r["score"] or 0 for r in data]
    slope = float(np.polyfit(z5_vals_num, sc_vals_num, 1)[0])

    recs = [
        (C["red"],   C["lred"],
         "INTENSIDAD",
         f"Cada minuto en Z5 te cuesta {abs(slope):.1f} pts de score. "
         f"Con Z5>10min duermes {abs(s_z5_high - s_z5_low):.0f} puntos peor "
         f"({s_z5_high:.0f} vs {s_z5_low:.0f}). Añade pausas largas entre series."),
        (C["blue"],  C["light"],
         "TIPO",
         f"La bici te da {abs(s_bici - s_pista):.0f} puntos mas de score que pista "
         f"({s_bici:.0f} vs {s_pista:.0f}). La vispera de competicion o "
         f"sesion importante, sustituye el running por bici Z2."),
        (C["green"], C["lgreen"],
         "PATRON OPTIMO",
         "Tus mejores noches comparten: Z5 < 5 min, sesion a las 17-18h, "
         "bici en Z3 o series cortas (4x300) con largas recuperaciones."),
        (C["amber"], C["lamber"],
         "TEMPERATURA",
         "En Valencia el calor no te perjudica — al contrario. "
         "La combinacion de fresco + alta intensidad (Z5 en invierno/primavera) "
         "es mas dura para tu recuperacion."),
    ]

    y0 = 0.95
    for border_c, bg_c, tag, text in recs:
        box = FancyBboxPatch((0.01, y0 - 0.21), 0.98, 0.19,
                             boxstyle="round,pad=0.01", linewidth=1.5,
                             edgecolor=border_c, facecolor=bg_c,
                             transform=ax_r.transAxes)
        ax_r.add_patch(box)
        ax_r.text(0.03, y0 - 0.04, tag, fontsize=8, fontweight="bold",
                  color=border_c, transform=ax_r.transAxes)
        ax_r.text(0.03, y0 - 0.13, text, fontsize=7.5, color=C["text"],
                  transform=ax_r.transAxes, wrap=True,
                  va="center")
        y0 -= 0.25

    pdf.savefig(fig, bbox_inches="tight")
    plt.close()


# ── PAGINA 5: Body Battery, Training Readiness y Estres ──────────────────────
def page_battery_readiness(pdf, data, fecha):
    fig = plt.figure(figsize=A4)
    fig.patch.set_facecolor(C["white"])
    header(fig, "BODY BATTERY, TRAINING READINESS Y ESTRES", 5, 6)
    footer(fig, fecha)

    gs = gridspec.GridSpec(2, 2, figure=fig,
                           top=0.89, bottom=0.08, left=0.10, right=0.95,
                           hspace=0.45, wspace=0.35)

    def scatter_trend(ax, xs_raw, ys_raw, title, xlabel, ylabel, color):
        pairs = [(x, y) for x, y in zip(xs_raw, ys_raw) if x is not None and y is not None]
        if not pairs:
            ax.set_title(title + "\n(sin datos aun)")
            ax.set_facecolor(C["lgray"])
            ax.text(0.5, 0.5, "Recarga el pipeline\npara obtener estos datos",
                    ha="center", va="center", transform=ax.transAxes,
                    fontsize=9, color=C["gray"])
            return
        xs, ys = zip(*pairs)
        ax.scatter(xs, ys, color=color, s=60, alpha=0.8,
                   edgecolors="white", linewidth=0.5)
        if len(xs) > 2 and len(set(xs)) > 1:
            try:
                z = np.polyfit(xs, ys, 1)
                p = np.poly1d(z)
                xr = np.linspace(min(xs), max(xs), 100)
                ax.plot(xr, p(xr), color=C["navy"], linewidth=1.5,
                        linestyle="--", label=f"Tend: {z[0]:+.1f} pts/unidad")
                ax.legend(fontsize=8)
            except np.linalg.LinAlgError:
                pass
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_facecolor(C["lgray"])

    # ── BB inicio de dia vs Score ─────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    scatter_trend(
        ax1,
        [r["bb_start"] for r in data],
        [r["score"]    for r in data],
        "Body Battery (manana) vs Score",
        "BB al despertar (0-100)",
        "Score de sueno (/100)",
        C["sky"]
    )

    # ── BB caida vs Score ─────────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    scatter_trend(
        ax2,
        [r["bb_drop"] for r in data],
        [r["score"]   for r in data],
        "Caida Body Battery vs Score",
        "Puntos de BB consumidos",
        "Score de sueno (/100)",
        C["amber"]
    )

    # ── Training Readiness vs Score ───────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    scatter_trend(
        ax3,
        [r["training_readiness"] for r in data],
        [r["score"]              for r in data],
        "Training Readiness vs Score",
        "Training Readiness (0-100)",
        "Score de sueno (/100)",
        C["green"]
    )

    # ── Estres vs Score ───────────────────────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    scatter_trend(
        ax4,
        [r["stress_avg"] for r in data],
        [r["score"]      for r in data],
        "Estres diario vs Score",
        "Nivel de estres medio",
        "Score de sueno (/100)",
        C["red"]
    )

    pdf.savefig(fig, bbox_inches="tight")
    plt.close()


def type_colors_map(t):
    return {"Bici": C["sky"], "Pista/Running": C["red"], "Paseo": C["green"]}.get(t, C["gray"])


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    fecha = datetime.today().strftime("%d/%m/%Y")
    filename = f"informe_garmin_{datetime.today().strftime('%Y%m%d')}.pdf"

    print("Obteniendo datos de Athena...")
    try:
        raw_sessions = _run(QUERY_SESSIONS)
        print("  Columnas Body Battery / Training Readiness: disponibles")
    except RuntimeError:
        print("  [!] Tabla sin nuevas columnas — usando query basica (recarga el pipeline para obtener BB/TR)")
        raw_sessions = _run(QUERY_SESSIONS_BASIC)
    raw_history  = _run(QUERY_HISTORY)
    data    = cast(raw_sessions)
    history = raw_history
    print(f"  {len(data)} sesiones con sueno | {len(history)} dias de historial")

    print(f"Generando PDF: {filename}")
    with PdfPages(filename) as pdf:
        pdf.infodict().update({
            "Title":   "Informe Garmin - Sueno y Recuperacion",
            "Author":  "Aisha del Tio",
            "Subject": "Analisis de entrenamiento y sueno",
        })
        print("  [1/6] Portada...")
        page_portada(pdf, data, fecha)

        print("  [2/6] Zonas FC y tipo...")
        page_zonas_tipo(pdf, data, fecha)

        print("  [3/6] Hora y temperatura...")
        page_hora_temp(pdf, data, fecha)

        print("  [4/6] Historial 60 dias...")
        page_historial(pdf, data, history, fecha)

        print("  [5/6] Body Battery y Training Readiness...")
        page_battery_readiness(pdf, data, fecha)

        print("  [6/6] Recomendaciones...")
        page_recs(pdf, data, fecha)

    print(f"\n[OK] PDF generado: {filename}")
    print(f"     Ruta completa: {os.path.abspath(filename)}")


if __name__ == "__main__":
    main()
