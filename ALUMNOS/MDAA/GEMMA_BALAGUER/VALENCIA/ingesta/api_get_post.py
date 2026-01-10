import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import psycopg
import requests
from datetime import datetime

# Variables de entorno
DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_NAME = os.environ.get("DB_NAME", "pruebadb")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
TARGET_POST_URL = os.environ.get("TARGET_POST_URL", "http://localhost:8001/receive")

# FastAPI
app = FastAPI(title="API GET & POST")

# Modelo de datos
class ValenbisiStation(BaseModel):
    address: str
    number: int
    open: str
    available: int
    free: int
    total: int
    ticket: str
    updated_at: str
    lon: Optional[float] = None
    lat: Optional[float] = None
    update_jcd: Optional[str] = None
    fetched_at: Optional[datetime] = None  # Nuevo campo

# Conexión a PostgreSQL
def get_db_connection():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

# Endpoint GET: obtiene los datos
@app.get("/stations", response_model=List[ValenbisiStation])
def get_stations(limit: int = 20):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT address, number, open, available, free, total, ticket, 
                   updated_at, lon, lat, update_jcd, fetched_at 
            FROM valenbisi
            ORDER BY fetched_at DESC
            LIMIT %s
        """, (limit,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        stations = [
            ValenbisiStation(
                address=row[0],
                number=row[1],
                open=row[2],
                available=row[3],
                free=row[4],
                total=row[5],
                ticket=row[6],
                updated_at=row[7],
                lon=row[8],
                lat=row[9],
                update_jcd=row[10],
                fetched_at=row[11]
            )
            for row in rows
        ]
        return stations

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint POST: enviar datos a otra API
@app.post("/send_to_target")
def send_to_target(limit: int = 20):
    stations = get_stations(limit=limit)
    try:
        payload = [station.dict() for station in stations]
        response = requests.post(TARGET_POST_URL, json=payload)
        response.raise_for_status()
        return {"status": "success", "sent_records": len(stations)}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar datos: {e}")
