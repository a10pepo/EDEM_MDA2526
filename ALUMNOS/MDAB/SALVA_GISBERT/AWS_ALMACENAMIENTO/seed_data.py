import argparse
import os
import random
from datetime import date, timedelta
from pathlib import Path

from db import connect


ROOT_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT_DIR / "schema.sql"

FIRST_NAMES = [
    "Adrian",
    "Alvaro",
    "Bruno",
    "Carlos",
    "Dario",
    "Diego",
    "Enzo",
    "Hector",
    "Iker",
    "Ivan",
    "Javier",
    "Leo",
    "Lucas",
    "Manuel",
    "Marcos",
    "Mario",
    "Nicolas",
    "Pablo",
    "Ruben",
    "Sergio",
    "Victor",
]

LAST_NAMES = [
    "Alonso",
    "Campos",
    "Delgado",
    "Fernandez",
    "Garcia",
    "Gomez",
    "Herrera",
    "Jimenez",
    "Lopez",
    "Martin",
    "Morales",
    "Navarro",
    "Ortega",
    "Perez",
    "Ramos",
    "Ruiz",
    "Sanchez",
    "Torres",
    "Vega",
]

OPPONENTS = [
    "Atletico Norte",
    "Union Ribera",
    "CD Monteluz",
    "Sporting Alameda",
    "Real Valdeverde",
    "CF Los Pinos",
    "Racing del Sur",
    "Deportivo Central",
    "Estrella Roja FC",
    "AD Mirador",
]

STADIUMS = [
    "Campo Municipal Las Encinas",
    "Estadio La Vega",
    "Campo Nuevo Horizonte",
    "Polideportivo San Isidro",
    "Ciudad Deportiva El Roble",
]

POSITIONS = ["goalkeeper", "defender", "midfielder", "forward"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate random data in an Amazon RDS PostgreSQL database."
    )
    parser.add_argument(
        "--players",
        type=int,
        default=24,
        help="Number of random players to create.",
    )
    parser.add_argument(
        "--matches",
        type=int,
        default=6,
        help="Number of random matches to create.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional seed to generate reproducible data.",
    )
    parser.add_argument(
        "--skip-schema",
        action="store_true",
        help="Do not recreate tables before inserting random data.",
    )
    return parser.parse_args()


def reset_database(connection):
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with connection.cursor() as cursor:
        cursor.execute(schema)
    connection.commit()


def random_player_name(used_names):
    while True:
        full_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        if full_name not in used_names:
            used_names.add(full_name)
            return full_name


def generate_players(count):
    players = []
    used_names = set()

    for _ in range(count):
        status = random.choices(
            ["available", "injured", "suspended"],
            weights=[78, 14, 8],
            k=1,
        )[0]
        review_days_ago = random.randint(20, 430)
        players.append(
            {
                "name": random_player_name(used_names),
                "age": random.randint(17, 38),
                "position": random.choices(
                    POSITIONS,
                    weights=[2, 8, 8, 5],
                    k=1,
                )[0],
                "status": status,
                "last_medical_review": date.today()
                - timedelta(days=review_days_ago),
            }
        )

    for player in players:
        player["last_medical_review"] = player["last_medical_review"].isoformat()

    return players


def generate_matches(count):
    matches = []
    used_opponents = set()

    for index in range(count):
        available_opponents = [
            opponent for opponent in OPPONENTS if opponent not in used_opponents
        ]
        if available_opponents:
            opponent = random.choice(available_opponents)
            used_opponents.add(opponent)
        else:
            opponent = f"{random.choice(OPPONENTS)} B"

        matches.append(
            {
                "opponent": opponent,
                "match_date": (
                    date.today() + timedelta(days=random.randint(-10, 75))
                ).isoformat(),
                "stadium": random.choice(STADIUMS),
                "max_callups": random.choice([16, 18, 20, 23]),
            }
        )

    matches.sort(key=lambda match: match["match_date"])
    return matches


def insert_players(connection, players):
    player_ids = []
    with connection.cursor() as cursor:
        for player in players:
            cursor.execute(
                """
                INSERT INTO players
                    (name, age, position, status, last_medical_review)
                VALUES
                    (%(name)s, %(age)s, %(position)s, %(status)s,
                    %(last_medical_review)s)
                RETURNING id
                """,
                player,
            )
            player_ids.append(cursor.fetchone()["id"])
    connection.commit()
    return player_ids


def insert_matches(connection, matches):
    match_ids = []
    with connection.cursor() as cursor:
        for match in matches:
            cursor.execute(
                """
                INSERT INTO matches (opponent, match_date, stadium, max_callups)
                VALUES (%(opponent)s, %(match_date)s, %(stadium)s, %(max_callups)s)
                RETURNING id
                """,
                match,
            )
            match_ids.append(cursor.fetchone()["id"])
    connection.commit()
    return match_ids


def build_callups(players, player_ids, match_ids, matches):
    callups = []
    players_by_id = dict(zip(player_ids, players))

    for match_id, match in zip(match_ids, matches):
        max_callups = min(match["max_callups"], len(player_ids))
        min_callups = min(9, max_callups)
        selected_count = random.randint(min_callups, max_callups)
        selected_player_ids = random.sample(player_ids, selected_count)
        shirt_numbers = random.sample(range(1, 100), selected_count)

        for player_id, shirt_number in zip(selected_player_ids, shirt_numbers):
            player = players_by_id[player_id]
            if player["status"] == "injured":
                callup_status = random.choices(
                    ["injured", "absent"],
                    weights=[85, 15],
                    k=1,
                )[0]
            elif player["status"] == "suspended":
                callup_status = "absent"
            else:
                callup_status = random.choices(
                    ["confirmed", "called", "absent"],
                    weights=[70, 20, 10],
                    k=1,
                )[0]

            callups.append(
                {
                    "match_id": match_id,
                    "player_id": player_id,
                    "callup_status": callup_status,
                    "shirt_number": shirt_number,
                }
            )

    return callups


def insert_callups(connection, callups):
    with connection.cursor() as cursor:
        cursor.executemany(
            """
            INSERT INTO callups
                (match_id, player_id, callup_status, shirt_number)
            VALUES
                (%(match_id)s, %(player_id)s, %(callup_status)s, %(shirt_number)s)
            """,
            callups,
        )
    connection.commit()


def main():
    args = parse_args()

    if args.players < 11:
        raise ValueError("At least 11 players are needed to generate useful callups.")
    if args.matches < 1:
        raise ValueError("At least 1 match is needed.")

    if args.seed is not None:
        random.seed(args.seed)

    connection = connect()
    try:
        if not args.skip_schema:
            reset_database(connection)

        players = generate_players(args.players)
        matches = generate_matches(args.matches)
        player_ids = insert_players(connection, players)
        match_ids = insert_matches(connection, matches)
        callups = build_callups(players, player_ids, match_ids, matches)
        insert_callups(connection, callups)
    finally:
        connection.close()

    print("Random data generated successfully.")
    print(f"Database host: {os.getenv('RDS_HOST') or os.getenv('DB_HOST')}")
    print(f"Database name: {os.getenv('RDS_DATABASE') or os.getenv('DB_NAME')}")
    print(f"Players: {len(players)}")
    print(f"Matches: {len(matches)}")
    print(f"Callups: {len(callups)}")


if __name__ == "__main__":
    main()
