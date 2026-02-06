from fastapi import FastAPI, HTTPException, Depends, Security, Query
from fastapi.security import APIKeyHeader
from config_env import *
import pandas as pd
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, Any
from sqlalchemy import types, text
from contextlib import asynccontextmanager
from database import init_db
from sqlalchemy.dialects.postgresql import insert
import math
from datetime import date
import base64
from pathlib import Path
from uuid import uuid4

IMAGE_PATH = Path("/data/images")
IMAGE_PATH.mkdir(parents=True, exist_ok=True)

class TicketCreate(BaseModel):
    ticket_id: int
    timestamp: str
    shop_name: str
    product_name: str
    address: str
    latitud: str
    longitud: str
    precio: float = Field(alias="import")
    product_image: Optional[str] = None
    refund_deadline: Optional[date] = None
    change_deadline: Optional[date] = None

    model_config = ConfigDict(
        extra='forbid',
        populate_by_name=True
    )
        
# ----------------------------------

@asynccontextmanager    # El decorador es un envoltorio funcional. Le dice a python que la función es un Gestor de Contexto (Context Manager) y tiene dos tiempos, una al arrancar (Antes del yield) y otra al apagar la api (Despues del yield)
async def lifespan(app: FastAPI):

    # --- CÓDIGO AL ARRANCAR EL CONTENEDOR ---

    try:
        init_db()
        # Cargar datos históricos (solo se ejecuta si la tabla está vacía)
        
    except Exception as e:
        print(f"❌ Error inicializando la BD: {e}")
    yield   #Pausa la ejecución de la función para seguir con la aplicación.
            #Se pueden configurar acciones a realizar al apagar la api

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

class TicketWrapper(BaseModel):
    ticket: TicketCreate

@app.post("/ingestion", status_code=201)
async def create_ticket(wrapper: TicketWrapper):
    ticket = wrapper.ticket

    # Guardar imagen si viene
    if ticket.product_image:
        try:
            image_bytes = base64.b64decode(ticket.product_image)
            filename = f"{ticket.ticket_id}_{uuid4().hex}.jpg"
            with open(IMAGE_PATH / filename, "wb") as f:
                f.write(image_bytes)
        except Exception as e:
            print(f"Error guardando imagen: {e}")

    query = text("""
        INSERT INTO raw.tickets (
            ticket_id, timestamp, address, shop_name, latitud, longitud,
            product_name, "import", refund_deadline, change_deadline
        ) VALUES (
            :ticket_id, :timestamp, :address, :shop_name, :latitud, :longitud,
            :product_name, :import, :refund_deadline, :change_deadline
        )
        ON CONFLICT (ticket_id) DO NOTHING
        RETURNING ticket_id;
    """)

    try:
        with engine.connect() as conn:
            with conn.begin():
                result = conn.execute(query, {
                    "ticket_id": ticket.ticket_id,
                    "timestamp": ticket.timestamp,
                    "address": ticket.address,
                    "shop_name": ticket.shop_name,
                    "latitud": ticket.latitud,
                    "longitud": ticket.longitud,
                    "product_name": ticket.product_name,
                    "import": ticket.precio,
                    "refund_deadline": ticket.refund_deadline,
                    "change_deadline": ticket.change_deadline,
                })
                row = result.fetchone()
                new_id = row[0] if row else ticket.ticket_id

        return {
            "status": "success",
            "message": "Ticket created successfully",
            "id_ticket": new_id
        }

    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during database insertion")

@app.get("/datos")
async def get_tickets():
    """
    Endpoint para obtener todos los tickets de la vista final.
    Devuelve un JSON con los datos listos para visualización.
    """
    query = text("SELECT * FROM public.ventas_finales;")
    
    try:
        with engine.connect() as conn:
            result = conn.execute(query)
            tickets = [dict(row) for row in result]
        return tickets

    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during data retrieval")