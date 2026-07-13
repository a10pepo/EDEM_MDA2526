import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

RECORD_WINS = 103


def get_conn():
    return psycopg2.connect(
        host=os.environ['RDS_HOST'],
        port=os.environ['RDS_PORT'],
        user=os.environ['RDS_USER'],
        password=os.environ['RDS_PASSWORD'],
        database=os.environ['RDS_DB'],
    )


def sep():
    print("-" * 50)


# --- LISTADOS ---

def list_pilots():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT rank, driver, nationality, wins, championships, years_active FROM pilots ORDER BY rank;")
        rows = cur.fetchall()
    print("\n=== PILOTOS ===")
    for r in rows:
        status = "Activo" if "present" in r[5] else "Retirado"
        print(f"[{r[0]}] {r[1]} | {r[2]} | Victorias: {r[3]} | Campeonatos: {r[4]} | {status}")
        sep()


def list_races():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT race_id, name, circuit, date, laps FROM races ORDER BY date;")
        rows = cur.fetchall()
    print("\n=== CARRERAS ===")
    for r in rows:
        print(f"[{r[0]}] {r[1]} | Circuito: {r[2]} | Fecha: {r[3]} | Vueltas: {r[4]}")
        sep()


def list_results():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT result_id, race_id, driver, position, points, status FROM results ORDER BY result_id;")
        rows = cur.fetchall()
    print("\n=== RESULTADOS ===")
    for r in rows:
        print(f"[{r[0]}] Carrera: {r[1]} | Piloto: {r[2]} | Posicion: {r[3]} | Puntos: {r[4]} | Estado: {r[5]}")
        sep()


# --- REGISTRO ---

def register_pilot():
    print("\n=== REGISTRAR PILOTO ===")
    data = (
        int(input("Posicion en ranking: ").strip()),
        input("Nombre del piloto: ").strip(),
        input("Nacionalidad: ").strip(),
        int(input("Victorias: ").strip()),
        int(input("Campeonatos: ").strip()),
        input("Anos en activo (ej. 2010-present): ").strip(),
        input("Equipo con mas victorias: ").strip(),
    )
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO pilots VALUES (%s,%s,%s,%s,%s,%s,%s);", data)
    print(f"Piloto {data[1]} registrado correctamente.")


def register_race():
    print("\n=== REGISTRAR CARRERA ===")
    data = (
        input("ID carrera (ej. R-011): ").strip(),
        input("Nombre del GP: ").strip(),
        input("Circuito: ").strip(),
        input("Fecha (YYYY-MM-DD): ").strip(),
        int(input("Numero de vueltas: ").strip()),
        int(input("Distancia total (km): ").strip()),
    )
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO races VALUES (%s,%s,%s,%s,%s,%s);", data)
    print(f"Carrera {data[1]} registrada correctamente.")


def register_result():
    print("\n=== REGISTRAR RESULTADO ===")
    data = (
        input("ID resultado (ej. RES-041): ").strip(),
        input("ID carrera: ").strip(),
        input("Nombre del piloto: ").strip(),
        int(input("Posicion final (0 si DNF): ").strip()),
        int(input("Puntos obtenidos: ").strip()),
        input("Estado (Finished/DNF/DNS): ").strip(),
    )
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO results VALUES (%s,%s,%s,%s,%s,%s);", data)
    print(f"Resultado registrado correctamente.")


# --- CONSULTAS ---

def check_days_since_last_race():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT p.driver,
                   CURRENT_DATE - MAX(r.date) AS days_since
            FROM pilots p
            LEFT JOIN results res ON p.driver = res.driver
            LEFT JOIN races r ON res.race_id = r.race_id
            GROUP BY p.driver
            ORDER BY days_since DESC NULLS FIRST;
        """)
        rows = cur.fetchall()
    print("\n=== DIAS DESDE ULTIMA CARRERA POR PILOTO ===")
    for r in rows:
        days = r[1] if r[1] is not None else "Sin carreras"
        print(f"[{r[0]}]: {days} dias")
        sep()


def check_wins_to_record():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT driver, wins FROM pilots ORDER BY rank;")
        rows = cur.fetchall()
    print(f"\n=== VICTORIAS PARA IGUALAR EL RECORD ({RECORD_WINS} - Hamilton) ===")
    for r in rows:
        diff = RECORD_WINS - r[1]
        if diff > 0:
            print(f"[{r[0]}]: Le faltan {diff} victorias")
        else:
            print(f"[{r[0]}]: ES EL RECORD o lo supera ({r[1]} victorias)")
        sep()


def check_pilot_status():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT driver, years_active FROM pilots ORDER BY rank;")
        rows = cur.fetchall()
    print("\n=== ESTADO DE PILOTOS ===")
    for r in rows:
        status = "Activo" if "present" in r[1] else "Retirado"
        print(f"[{r[0]}]: {status} | {r[1]}")
        sep()


# --- ALERTAS ---

def alert_high_dnf_rate():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT driver,
                   COUNT(*) AS total,
                   SUM(CASE WHEN status = 'DNF' THEN 1 ELSE 0 END) AS dnfs,
                   round(SUM(CASE WHEN status = 'DNF' THEN 1 ELSE 0 END)::numeric / COUNT(*) * 100, 1) AS dnf_pct
            FROM results
            GROUP BY driver
            HAVING SUM(CASE WHEN status = 'DNF' THEN 1 ELSE 0 END)::float / COUNT(*) > 0.10
            ORDER BY dnf_pct DESC;
        """)
        rows = cur.fetchall()
    print("\n=== ALERTA: TASA DE DNF > 10% ===")
    if not rows:
        print("Sin alertas.")
    for r in rows:
        print(f"[!] [{r[0]}]: {r[2]}/{r[1]} DNFs ({r[3]}%)")


def alert_retired_pilots():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT driver, years_active FROM pilots WHERE years_active NOT LIKE '%present%' ORDER BY rank;")
        rows = cur.fetchall()
    print("\n=== ALERTA: PILOTOS RETIRADOS ===")
    if not rows:
        print("Todos los pilotos estan activos.")
    for r in rows:
        print(f"[!] [{r[0]}]: Retirado | {r[1]}")


def alert_dominant_pilots():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT driver, wins,
                   round(wins::numeric / {RECORD_WINS} * 100, 1) AS pct
            FROM pilots
            WHERE wins::float / {RECORD_WINS} >= 0.10
            ORDER BY wins DESC;
        """)
        rows = cur.fetchall()
    print(f"\n=== ALERTA: PILOTOS CON MAS DEL 10% DEL RECORD ({RECORD_WINS}) ===")
    if not rows:
        print("Sin alertas.")
    for r in rows:
        print(f"[!] [{r[0]}]: {r[1]} victorias ({r[2]}% del record)")


# --- MENU ---

def menu():
    options = {
        "1":  ("Ver lista de pilotos", list_pilots),
        "2":  ("Ver lista de carreras", list_races),
        "3":  ("Ver lista de resultados", list_results),
        "4":  ("Registrar piloto", register_pilot),
        "5":  ("Registrar carrera", register_race),
        "6":  ("Registrar resultado", register_result),
        "7":  ("Dias desde ultima carrera por piloto", check_days_since_last_race),
        "8":  ("Victorias para igualar el record", check_wins_to_record),
        "9":  ("Estado de pilotos", check_pilot_status),
        "10": ("Alerta: tasa de DNF alta", alert_high_dnf_rate),
        "11": ("Alerta: pilotos retirados", alert_retired_pilots),
        "12": ("Alerta: pilotos dominantes", alert_dominant_pilots),
        "0":  ("Salir", None),
    }

    while True:
        print("\n========== GESTOR F1 (AWS RDS) ==========")
        for key, (label, _) in options.items():
            print(f"  {key}. {label}")
        print("==========================================")
        choice = input("Selecciona una opcion: ").strip()

        if choice == "0":
            print("Hasta luego.")
            break
        elif choice in options:
            options[choice][1]()
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    menu()
