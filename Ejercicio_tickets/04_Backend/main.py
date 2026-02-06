from fastapi import FastAPI, HTTPException, Depends, Security, Query
from fastapi.security import APIKeyHeader
from config_env import *
import pandas as pd
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from sqlalchemy import types, text
from contextlib import asynccontextmanager
from database import init_db, load_historical_real_data, load_historical_simulated_data
from sqlalchemy.dialects.postgresql import insert
import math

# ----------------------------------

# Inicialización de la API
app = FastAPI(
    lifespan=lifespan,
    title="Tickets security API",
    description="API de aislamiento para proteger el acceso a {POSTGRES_DB}",
    version="1.0.0"
)

# ----------------------------------

# --- ENDPOINTS ---

@app.get("/health")
async def health_check():
    """
    Endpoint de salud para verificar que el backend está operativo.
    Verifica conexión a la base de datos.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {e}")


# --- ENDPOINTS INGESTA ---

@app.post("/ingestion/", status_code=201)
async def create_ticket(ticket: TicketCreate):
    """
    Endpoint to insert a new ticket record into the raw.tickets table.
    """
    query = text("""
        INSERT INTO raw.tickets (
            ticket_id, timestamp, adress, shop_name, latitud, longitud, product_name, import, refund_deadline, change_deadline)
        VALUES (
            :ticket_id, :timestamp, :adress, :shop_name, :latitud, :longitud, :product_name, :import, :refund_deadline, :change_deadline
        )
        ON CONFLICT (ticket_id) DO NOTHING;
    """)
    
    try:
        # Establish connection and execute the insert
        with engine.connect() as conn:
            # We use a transaction to ensure data integrity
            with conn.begin():
                result = conn.execute(query, {
                    "purchase_date": ticket.purchase_date,
                    "price": ticket.price,
                    "shop": ticket.shop
                })
                # Fetch the generated ID
                new_id = result.fetchone()[0]
                
        return {
            "status": "success",
            "message": "Ticket created successfully",
            "id_ticket": new_id
        }

    except Exception as e:
        # Log the error and return a 500 status code
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during database insertion")
