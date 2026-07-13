from flask import Flask, render_template, jsonify, request
from datetime import date, datetime
from database import init_db, fetch_all, fetch_one, execute_write

app = Flask(__name__)
MINUTOS_TEMPORADA = 3060


def enrich(jugadores):
    hoy = date.today()
    for j in jugadores:
        try:
            proximo = datetime.strptime(j["fecha_proximo_partido"], "%Y-%m-%d").date()
            j["dias_restantes"] = (proximo - hoy).days
        except Exception:
            j["dias_restantes"] = 999
        try:
            j["pct_minutos"] = round(j["minutos_jugados"] / MINUTOS_TEMPORADA * 100, 1)
        except Exception:
            j["pct_minutos"] = 0
    return jugadores


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/jugadores", methods=["GET"])
def get_jugadores():
    jugadores = fetch_all("SELECT * FROM jugadores ORDER BY Posicion")
    return jsonify(enrich(jugadores))


@app.route("/api/jugadores", methods=["POST"])
def add_jugador():
    data = request.json
    ultimo = fetch_one("SELECT MAX(CAST(REPLACE(id_jugador,'JUG','') AS INTEGER)) AS max_id FROM jugadores")
    nuevo_id = f"JUG{str((ultimo['max_id'] or 0) + 1).zfill(3)}"
    nueva_pos = fetch_one("SELECT COUNT(*) AS total FROM jugadores")["total"] + 1

    execute_write("""
        INSERT INTO jugadores VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, [
        nuevo_id, nueva_pos,
        data.get("Nombre", ""),
        data.get("Nacionalidad", ""),
        data.get("Club_Actual", ""),
        int(data.get("Edad", 0)),
        data.get("Posicion_Campo", ""),
        int(data.get("Balones_de_Oro", 0)),
        data.get("fecha_nacimiento", ""),
        data.get("fecha_ultimo_partido", ""),
        data.get("fecha_proximo_partido", ""),
        float(data.get("salario_anual_millones", 0)),
        float(data.get("valor_mercado_millones", 0)),
        int(data.get("goles_temporada", 0)),
        int(data.get("asistencias_temporada", 0)),
        int(data.get("minutos_jugados", 0)),
        data.get("estado", "activo"),
    ])
    return jsonify({"id_jugador": nuevo_id, **data}), 201


@app.route("/api/jugadores/<id_jugador>", methods=["PUT"])
def update_jugador(id_jugador):
    data = request.json
    jugador = fetch_one("SELECT * FROM jugadores WHERE id_jugador = ?", [id_jugador])
    if not jugador:
        return jsonify({"error": "No encontrado"}), 404

    execute_write("""
        UPDATE jugadores SET
            Nombre                 = ?,
            Nacionalidad           = ?,
            Club_Actual            = ?,
            Edad                   = ?,
            Posicion_Campo         = ?,
            Balones_de_Oro         = ?,
            fecha_nacimiento       = ?,
            fecha_ultimo_partido   = ?,
            fecha_proximo_partido  = ?,
            salario_anual_millones = ?,
            valor_mercado_millones = ?,
            goles_temporada        = ?,
            asistencias_temporada  = ?,
            minutos_jugados        = ?,
            estado                 = ?
        WHERE id_jugador = ?
    """, [
        data.get("Nombre", jugador["Nombre"]),
        data.get("Nacionalidad", jugador["Nacionalidad"]),
        data.get("Club_Actual", jugador["Club_Actual"]),
        int(data.get("Edad", jugador["Edad"])),
        data.get("Posicion_Campo", jugador["Posicion_Campo"]),
        int(data.get("Balones_de_Oro", jugador["Balones_de_Oro"])),
        data.get("fecha_nacimiento", jugador["fecha_nacimiento"]),
        data.get("fecha_ultimo_partido", jugador["fecha_ultimo_partido"]),
        data.get("fecha_proximo_partido", jugador["fecha_proximo_partido"]),
        float(data.get("salario_anual_millones", jugador["salario_anual_millones"])),
        float(data.get("valor_mercado_millones", jugador["valor_mercado_millones"])),
        int(data.get("goles_temporada", jugador["goles_temporada"])),
        int(data.get("asistencias_temporada", jugador["asistencias_temporada"])),
        int(data.get("minutos_jugados", jugador["minutos_jugados"])),
        data.get("estado", jugador["estado"]),
        id_jugador,
    ])
    return jsonify(fetch_one("SELECT * FROM jugadores WHERE id_jugador = ?", [id_jugador]))


@app.route("/api/alertas", methods=["GET"])
def get_alertas():
    jugadores = fetch_all("SELECT * FROM jugadores")
    hoy = date.today()
    result = {"proximo_partido": [], "lesionados": [], "salario": []}

    for j in jugadores:
        try:
            dias = (datetime.strptime(j["fecha_proximo_partido"], "%Y-%m-%d").date() - hoy).days
            if dias < 100:
                result["proximo_partido"].append({**j, "dias_restantes": dias})
        except Exception:
            pass

    for j in jugadores:
        if j["estado"] == "lesionado":
            pct = j["minutos_jugados"] / MINUTOS_TEMPORADA * 100
            if pct < 30:
                result["lesionados"].append({**j, "pct_minutos": round(pct, 1)})

    totales = fetch_all("SELECT Club_Actual, SUM(salario_anual_millones) AS total FROM jugadores GROUP BY Club_Actual")
    total_por_club = {r["Club_Actual"]: r["total"] for r in totales}

    for j in jugadores:
        total = total_por_club.get(j["Club_Actual"], 1) or 1
        pct = j["salario_anual_millones"] / total * 100
        if pct > 10:
            result["salario"].append({**j, "pct_salario": round(pct, 1), "total_club": total})

    return jsonify(result)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
