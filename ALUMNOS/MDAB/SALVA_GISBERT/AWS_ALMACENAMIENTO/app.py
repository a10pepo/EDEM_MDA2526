import argparse
from datetime import date

from db import connect, query_all, query_one

POSITION_LABELS = {
    "goalkeeper": "Portero",
    "defender": "Defensa",
    "midfielder": "Centrocampista",
    "forward": "Delantero",
}

STATUS_LABELS = {
    "available": "Disponible",
    "injured": "Lesionado",
    "suspended": "Sancionado",
    "called": "Convocado",
    "confirmed": "Confirmado",
    "absent": "Ausente",
}


def parse_args():
    parser = argparse.ArgumentParser(description="Football Callup Manager CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("players", help="Show registered players.")
    subparsers.add_parser("matches", help="Show registered matches.")

    callups_parser = subparsers.add_parser("callups", help="Show callups for a match.")
    callups_parser.add_argument("match_id", type=int, help="Match id.")

    subparsers.add_parser("alerts", help="Show business alerts.")
    return parser.parse_args()


def print_table(headers, rows):
    if not rows:
        print("No hay datos para mostrar.")
        return

    widths = [
        max(len(str(header)), *(len(str(row[index])) for row in rows))
        for index, header in enumerate(headers)
    ]

    header_line = " | ".join(
        str(header).ljust(widths[index]) for index, header in enumerate(headers)
    )
    separator = "-+-".join("-" * width for width in widths)
    print(header_line)
    print(separator)

    for row in rows:
        print(
            " | ".join(
                str(value).ljust(widths[index]) for index, value in enumerate(row)
            )
        )


def show_players(connection):
    rows = query_all(
        connection,
        """
        SELECT id, name, age, position, status, last_medical_review
        FROM players
        ORDER BY position, name
        """
    )

    table_rows = [
        (
            row["id"],
            row["name"],
            row["age"],
            POSITION_LABELS[row["position"]],
            STATUS_LABELS[row["status"]],
            row["last_medical_review"],
        )
        for row in rows
    ]
    print_table(
        ["ID", "Jugador", "Edad", "Posicion", "Estado", "Revision medica"],
        table_rows,
    )


def fetch_match_summary(connection):
    return query_all(
        connection,
        """
        SELECT
            m.id,
            m.opponent,
            m.match_date,
            m.stadium,
            m.max_callups,
            COUNT(c.id) AS total_callups,
            COALESCE(SUM(CASE WHEN c.callup_status = 'confirmed' THEN 1 ELSE 0 END), 0)
                AS confirmed_players
        FROM matches m
        LEFT JOIN callups c ON c.match_id = m.id
        GROUP BY m.id, m.opponent, m.match_date, m.stadium, m.max_callups
        ORDER BY m.match_date
        """
    )


def show_matches(connection):
    rows = fetch_match_summary(connection)
    table_rows = []

    for row in rows:
        free_spots = row["max_callups"] - row["total_callups"]
        table_rows.append(
            (
                row["id"],
                row["opponent"],
                row["match_date"],
                row["stadium"],
                row["max_callups"],
                row["total_callups"],
                row["confirmed_players"],
                free_spots,
            )
        )

    print_table(
        [
            "ID",
            "Rival",
            "Fecha",
            "Estadio",
            "Max",
            "Convocados",
            "Confirmados",
            "Libres",
        ],
        table_rows,
    )


def show_callups(connection, match_id):
    match = query_one(
        connection,
        "SELECT opponent, match_date FROM matches WHERE id = %s",
        (match_id,),
    )

    if match is None:
        print(f"No existe ningun partido con id {match_id}.")
        return

    print(f"Convocatoria vs {match['opponent']} ({match['match_date']})")
    rows = query_all(
        connection,
        """
        SELECT
            c.shirt_number,
            p.name,
            p.position,
            p.status AS player_status,
            c.callup_status
        FROM callups c
        JOIN players p ON p.id = c.player_id
        WHERE c.match_id = %s
        ORDER BY c.shirt_number
        """,
        (match_id,),
    )

    table_rows = [
        (
            row["shirt_number"],
            row["name"],
            POSITION_LABELS[row["position"]],
            STATUS_LABELS[row["player_status"]],
            STATUS_LABELS[row["callup_status"]],
        )
        for row in rows
    ]
    print_table(["Dorsal", "Jugador", "Posicion", "Estado", "Convocatoria"], table_rows)


def show_alerts(connection):
    alerts = []

    for row in fetch_match_summary(connection):
        free_spots = row["max_callups"] - row["total_callups"]
        free_percentage = free_spots / row["max_callups"]

        if row["confirmed_players"] < 11:
            alerts.append(
                "PARTIDO: "
                f"{row['opponent']} ({row['match_date']}) tiene "
                f"{row['confirmed_players']} jugadores confirmados. Minimo: 11."
            )

        if free_percentage > 0.10:
            alerts.append(
                "CONVOCATORIA: "
                f"{row['opponent']} ({row['match_date']}) tiene {free_spots} "
                f"plazas libres de {row['max_callups']} "
                f"({free_percentage:.0%})."
            )

    medical_rows = query_all(
        connection,
        """
        SELECT id, name, last_medical_review
        FROM players
        ORDER BY last_medical_review
        """
    )

    for row in medical_rows:
        review_value = row["last_medical_review"]
        review_date = (
            review_value
            if isinstance(review_value, date)
            else date.fromisoformat(str(review_value))
        )
        days_without_review = (date.today() - review_date).days
        if days_without_review > 365:
            alerts.append(
                "REVISION MEDICA: "
                f"{row['name']} lleva {days_without_review} dias sin revision."
            )

    if not alerts:
        print("No hay alertas activas.")
        return

    for alert in alerts:
        print(f"- {alert}")


def main():
    args = parse_args()
    connection = connect()
    try:
        if args.command == "players":
            show_players(connection)
        elif args.command == "matches":
            show_matches(connection)
        elif args.command == "callups":
            show_callups(connection, args.match_id)
        elif args.command == "alerts":
            show_alerts(connection)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
