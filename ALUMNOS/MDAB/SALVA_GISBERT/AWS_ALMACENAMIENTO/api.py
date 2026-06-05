import os
from datetime import date

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import connect, query_all


app = FastAPI(title="Football Callup Manager API")

allowed_origins = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://127.0.0.1:5173,http://localhost:5173",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/players")
def list_players():
    connection = connect()
    try:
        return query_all(
            connection,
            """
            SELECT id, name, age, position, status, last_medical_review
            FROM players
            ORDER BY position, name
            """
        )
    finally:
        connection.close()


@app.get("/api/matches")
def list_matches():
    connection = connect()
    try:
        return query_all(
            connection,
            """
            SELECT id, opponent, match_date, stadium, max_callups
            FROM matches
            ORDER BY match_date
            """
        )
    finally:
        connection.close()


@app.get("/api/callups")
def list_callups():
    connection = connect()
    try:
        return query_all(
            connection,
            """
            SELECT
                c.id,
                c.match_id,
                c.player_id,
                c.callup_status,
                c.shirt_number,
                p.name AS player_name,
                p.position,
                p.status AS player_status
            FROM callups c
            JOIN players p ON p.id = c.player_id
            ORDER BY c.match_id, c.shirt_number
            """
        )
    finally:
        connection.close()


@app.get("/api/matches/{match_id}/callups")
def list_match_callups(match_id: int):
    connection = connect()
    try:
        return query_all(
            connection,
            """
            SELECT
                c.id,
                c.match_id,
                c.player_id,
                c.callup_status,
                c.shirt_number,
                p.name AS player_name,
                p.position,
                p.status AS player_status
            FROM callups c
            JOIN players p ON p.id = c.player_id
            WHERE c.match_id = %s
            ORDER BY c.shirt_number
            """,
            (match_id,),
        )
    finally:
        connection.close()


@app.get("/api/alerts")
def list_alerts():
    alerts = []

    connection = connect()
    try:
        matches = fetch_match_summary(connection)
        players = query_all(
            connection,
            """
            SELECT id, name, last_medical_review
            FROM players
            ORDER BY last_medical_review
            """
        )
    finally:
        connection.close()

    for match in matches:
        free_spots = match["max_callups"] - match["total_callups"]
        free_percentage = free_spots / match["max_callups"]

        if match["confirmed_players"] < 11:
            alerts.append(
                {
                    "id": f"confirmed-{match['id']}",
                    "type": "Partido",
                    "severity": "critical",
                    "title": f"{match['opponent']} necesita titulares",
                    "detail": (
                        f"{match['confirmed_players']} confirmados de 11 minimos "
                        f"para el {match['match_date']}."
                    ),
                }
            )

        if free_percentage > 0.10:
            alerts.append(
                {
                    "id": f"free-{match['id']}",
                    "type": "Convocatoria",
                    "severity": "warning",
                    "title": f"{match['opponent']} tiene huecos libres",
                    "detail": (
                        f"{free_spots} plazas libres de {match['max_callups']} "
                        f"({round(free_percentage * 100)}%)."
                    ),
                }
            )

    for player in players:
        review_value = player["last_medical_review"]
        review_date = (
            review_value
            if isinstance(review_value, date)
            else date.fromisoformat(str(review_value))
        )
        days_without_review = (date.today() - review_date).days

        if days_without_review > 365:
            alerts.append(
                {
                    "id": f"medical-{player['id']}",
                    "type": "Revision medica",
                    "severity": "warning",
                    "title": f"{player['name']} necesita revision",
                    "detail": f"{days_without_review} dias desde la ultima revision.",
                }
            )

    return alerts
