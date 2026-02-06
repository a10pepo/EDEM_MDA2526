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

class TicketCreate(BaseModel):
    # Identificadores (Basados en el JSON del script)
    # Usamos Field(alias=...) porque el script envía nombres distintos a los de la DB
    ticket_id: int = Field(alias="ticket_id")
    timestamp: str = Field(alias="timestamp") # "2024-06-01 11:00:00"
    
    # Contexto de la tienda y producto
    shop_name: str = Field(alias="shop_name")
    product_name: str = Field(alias="product_name")
    direccion: str = Field(alias="adress") # Mapea el error 'adress' del script
    
    # Valores numéricos
    precio: float = Field(alias="import")
    
    # Fechas (Opcionales para evitar errores si el generador fallara)
    refund_deadline: Optional[date] = Field(default=None, alias="refund_deadline")
    change_deadline: Optional[date] = Field(default=None, alias="change_deadline")

    # Si en el futuro el script enviara coordenadas, podrías usarlas así:
    # geo_point_2d: Optional[Dict[str, Any]] = None

    # CONFIGURACIÓN DE SEGURIDAD
    # 'forbid' asegura que si el script envía un campo no definido, FastAPI lo rechace
    # 'populate_by_name' permite usar tanto 'precio' como 'import' en el código
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
