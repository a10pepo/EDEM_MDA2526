import csv
import os
from datetime import date, datetime

CSV_PATH = os.path.join(os.path.dirname(__file__), "mejores_futbolistas.csv")

FIELDNAMES = [
    "id_jugador", "Posicion", "Nombre", "Nacionalidad", "Club_Actual",
    "Edad", "Posicion_Campo", "Balones_de_Oro", "fecha_nacimiento",
    "fecha_ultimo_partido", "fecha_proximo_partido", "salario_anual_millones",
    "valor_mercado_millones", "goles_temporada", "asistencias_temporada",
    "minutos_jugados", "estado"
]


def cargar_jugadores():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def guardar_jugadores(jugadores):
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(jugadores)


def listar_jugadores(jugadores):
    print(f"\n{'ID':<8} {'Nombre':<30} {'Club':<25} {'Pos.':<15} {'Estado'}")
    print("-" * 90)
    for j in jugadores:
        print(f"{j['id_jugador']:<8} {j['Nombre']:<30} {j['Club_Actual']:<25} {j['Posicion_Campo']:<15} {j['estado']}")


def listar_partidos(jugadores):
    print(f"\n{'ID':<8} {'Nombre':<30} {'Ultimo partido':<18} {'Proximo partido':<18} {'Dias restantes'}")
    print("-" * 95)
    hoy = date.today()
    for j in jugadores:
        proximo = datetime.strptime(j["fecha_proximo_partido"], "%Y-%m-%d").date()
        dias = (proximo - hoy).days
        print(f"{j['id_jugador']:<8} {j['Nombre']:<30} {j['fecha_ultimo_partido']:<18} {j['fecha_proximo_partido']:<18} {dias}")


def listar_estadisticas(jugadores):
    print(f"\n{'ID':<8} {'Nombre':<30} {'Goles':<8} {'Asist.':<8} {'Minutos':<10} {'Salario (M€)':<14} {'Valor (M€)'}")
    print("-" * 100)
    for j in jugadores:
        print(f"{j['id_jugador']:<8} {j['Nombre']:<30} {j['goles_temporada']:<8} {j['asistencias_temporada']:<8} {j['minutos_jugados']:<10} {j['salario_anual_millones']:<14} {j['valor_mercado_millones']}")


def registrar_jugador(jugadores):
    print("\n--- Registrar nuevo jugador ---")
    ultimo_id = max(int(j["id_jugador"].replace("JUG", "")) for j in jugadores)
    nuevo_id = f"JUG{str(ultimo_id + 1).zfill(3)}"

    jugador = {
        "id_jugador": nuevo_id,
        "Posicion": str(len(jugadores) + 1),
        "Nombre": input("Nombre: "),
        "Nacionalidad": input("Nacionalidad: "),
        "Club_Actual": input("Club actual: "),
        "Edad": input("Edad: "),
        "Posicion_Campo": input("Posicion en campo (Delantero/Extremo/Centrocampista/Defensa/Portero): "),
        "Balones_de_Oro": input("Balones de Oro: "),
        "fecha_nacimiento": input("Fecha de nacimiento (YYYY-MM-DD): "),
        "fecha_ultimo_partido": input("Fecha ultimo partido (YYYY-MM-DD): "),
        "fecha_proximo_partido": input("Fecha proximo partido (YYYY-MM-DD): "),
        "salario_anual_millones": input("Salario anual (millones €): "),
        "valor_mercado_millones": input("Valor de mercado (millones €): "),
        "goles_temporada": input("Goles esta temporada: "),
        "asistencias_temporada": input("Asistencias esta temporada: "),
        "minutos_jugados": input("Minutos jugados: "),
        "estado": input("Estado (activo/lesionado): "),
    }

    jugadores.append(jugador)
    guardar_jugadores(jugadores)
    print(f"\nJugador {jugador['Nombre']} registrado con ID {nuevo_id}.")
    return jugadores


def registrar_partido(jugadores):
    print("\n--- Registrar partido para un jugador ---")
    id_buscado = input("ID del jugador (ej. JUG001): ").strip()
    jugador = next((j for j in jugadores if j["id_jugador"] == id_buscado), None)

    if not jugador:
        print("Jugador no encontrado.")
        return jugadores

    print(f"Jugador: {jugador['Nombre']}")
    jugador["fecha_ultimo_partido"] = input("Fecha del partido jugado (YYYY-MM-DD): ")
    jugador["fecha_proximo_partido"] = input("Fecha del proximo partido (YYYY-MM-DD): ")
    jugador["estado"] = input("Estado tras el partido (activo/lesionado): ")

    guardar_jugadores(jugadores)
    print("Partido registrado correctamente.")
    return jugadores


def registrar_estadisticas(jugadores):
    print("\n--- Registrar estadisticas de un jugador ---")
    id_buscado = input("ID del jugador (ej. JUG001): ").strip()
    jugador = next((j for j in jugadores if j["id_jugador"] == id_buscado), None)

    if not jugador:
        print("Jugador no encontrado.")
        return jugadores

    print(f"Jugador: {jugador['Nombre']} | Goles actuales: {jugador['goles_temporada']} | Asist.: {jugador['asistencias_temporada']}")
    jugador["goles_temporada"] = input("Goles totales temporada: ")
    jugador["asistencias_temporada"] = input("Asistencias totales temporada: ")
    jugador["minutos_jugados"] = input("Minutos jugados totales: ")

    guardar_jugadores(jugadores)
    print("Estadisticas actualizadas.")
    return jugadores


MINUTOS_TEMPORADA = 3060  # 34 jornadas x 90 min


def dias_proximo_partido(jugadores):
    print("\n--- Dias hasta el proximo partido ---")
    id_buscado = input("ID del jugador (ej. JUG001) o ENTER para ver todos: ").strip()
    hoy = date.today()

    if id_buscado:
        subset = [j for j in jugadores if j["id_jugador"] == id_buscado]
        if not subset:
            print("Jugador no encontrado.")
            return
    else:
        subset = jugadores

    print(f"\n{'ID':<8} {'Nombre':<30} {'Proximo partido':<18} {'Dias restantes'}")
    print("-" * 70)
    for j in subset:
        proximo = datetime.strptime(j["fecha_proximo_partido"], "%Y-%m-%d").date()
        dias = (proximo - hoy).days
        aviso = " *** MENOS DE 7 DIAS ***" if dias < 7 else ""
        print(f"{j['id_jugador']:<8} {j['Nombre']:<30} {j['fecha_proximo_partido']:<18} {dias}{aviso}")


def consultar_estado(jugadores):
    print("\n--- Estado actual de los jugadores ---")
    id_buscado = input("ID del jugador (ej. JUG001) o ENTER para ver todos: ").strip()

    subset = [j for j in jugadores if j["id_jugador"] == id_buscado] if id_buscado else jugadores

    if id_buscado and not subset:
        print("Jugador no encontrado.")
        return

    print(f"\n{'ID':<8} {'Nombre':<30} {'Estado':<12} {'Minutos jugados':<18} {'% temporada jugado'}")
    print("-" * 85)
    for j in subset:
        minutos = int(j["minutos_jugados"])
        pct = round(minutos / MINUTOS_TEMPORADA * 100, 1)
        print(f"{j['id_jugador']:<8} {j['Nombre']:<30} {j['estado']:<12} {j['minutos_jugados']:<18} {pct}%")


def alertas(jugadores):
    hoy = date.today()
    inicio_temporada = date(2025, 8, 1)
    dias_temporada = (hoy - inicio_temporada).days or 1

    print("\n========== ALERTAS ==========")

    # Alerta 1: proximo partido en menos de 100 dias
    print("\n[!] Jugadores con proximo partido en menos de 100 dias:")
    encontrados = False
    for j in jugadores:
        proximo = datetime.strptime(j["fecha_proximo_partido"], "%Y-%m-%d").date()
        dias = (proximo - hoy).days
        if dias < 100:
            print(f"  - {j['Nombre']} ({j['Club_Actual']}): {dias} dias  [{j['estado']}]")
            encontrados = True
    if not encontrados:
        print("  Ninguno.")

    # Alerta 2: jugadores lesionados con pocos minutos (menos del 30% de la temporada)
    print("\n[!] Jugadores lesionados con menos del 30% de minutos jugados:")
    encontrados = False
    for j in jugadores:
        if j["estado"] == "lesionado":
            pct = int(j["minutos_jugados"]) / MINUTOS_TEMPORADA * 100
            if pct < 30:
                print(f"  - {j['Nombre']} ({j['Club_Actual']}): {round(pct, 1)}% minutos jugados")
                encontrados = True
    if not encontrados:
        print("  Ninguno.")

    # Alerta 3: jugadores cuyo salario supera el 10% del total de salarios del club
    print("\n[!] Jugadores cuyo salario supera el 10% del total salarial de su club:")
    encontrados = False
    clubes = {}
    for j in jugadores:
        club = j["Club_Actual"]
        clubes.setdefault(club, 0)
        clubes[club] += float(j["salario_anual_millones"])

    for j in jugadores:
        salario = float(j["salario_anual_millones"])
        total_club = clubes[j["Club_Actual"]]
        pct = salario / total_club * 100
        if pct > 10:
            print(f"  - {j['Nombre']} ({j['Club_Actual']}): {round(pct, 1)}% del presupuesto salarial del club ({salario}M€ de {total_club}M€)")
            encontrados = True
    if not encontrados:
        print("  Ninguno.")

    print("\n=============================")


def menu():
    jugadores = cargar_jugadores()

    while True:
        print("\n========== GESTOR DE FUTBOLISTAS ==========")
        print("--- Sprint 1: Registros y listados ---")
        print("1. Ver lista de jugadores")
        print("2. Ver lista de partidos (fechas)")
        print("3. Ver estadisticas de jugadores")
        print("4. Registrar nuevo jugador")
        print("5. Registrar partido jugado")
        print("6. Registrar estadisticas")
        print("--- Sprint 2: Consultas y alertas ---")
        print("7. Dias hasta el proximo partido")
        print("8. Consultar estado de jugadores")
        print("9. Ver todas las alertas")
        print("0. Salir")
        print("===========================================")

        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            listar_jugadores(jugadores)
        elif opcion == "2":
            listar_partidos(jugadores)
        elif opcion == "3":
            listar_estadisticas(jugadores)
        elif opcion == "4":
            jugadores = registrar_jugador(jugadores)
        elif opcion == "5":
            jugadores = registrar_partido(jugadores)
        elif opcion == "6":
            jugadores = registrar_estadisticas(jugadores)
        elif opcion == "7":
            dias_proximo_partido(jugadores)
        elif opcion == "8":
            consultar_estado(jugadores)
        elif opcion == "9":
            alertas(jugadores)
        elif opcion == "0":
            print("Hasta luego!")
            break
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    menu()
