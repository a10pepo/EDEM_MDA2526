from fastapi import FastAPI, HTTPException, Depends, Security, Query
from fastapi.security import APIKeyHeader
from config import engine
import pandas as pd
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from sqlalchemy import types, text
from contextlib import asynccontextmanager
from database import init_db, load_historical_real_data, load_historical_simulated_data
from sqlalchemy.dialects.postgresql import insert
import math


# ----------------------------------

# Clase principal de la medición
class AirQualityInbound(BaseModel):
    # Identificadores (Obligatorios)
    objectid: int
    fiwareid: str
    nombre: str
    direccion: str
    
    # Contexto de la zona
    tipozona: str
    tipoemisio: str
    calidad_am: str
    fecha_carg: str
    
    # Parámetros descriptivos (Pueden ser nulos en el JSON)
    parametros: Optional[str] = None
    mediciones: Optional[str] = None

    # Mediciones de Contaminantes (Opcionales para evitar errores si falta alguno)
    so2: Optional[float] = None
    no2: Optional[float] = None
    o3: Optional[float] = None
    co: Optional[float] = None
    pm10: Optional[float] = None
    pm25: Optional[float] = None

    # Geografía: Definidos como diccionarios genéricos por ahora
    # Solo validamos que sea un diccionario, no miramos qué hay dentro.

    geo_shape: Dict[str, Any]   # Le decimos a pylance que la clave del diccionario debe ser string pero el valor asociado a la clave puede ser cualquiera
    geo_point_2d: Dict[str, Any]

    # CONFIGURACIÓN DE SEGURIDAD
    # 'forbid' asegura que no aceptamos ningún campo nuevo que no esté en esta lista

    model_config = ConfigDict(extra='forbid')

# ----------------------------------

@asynccontextmanager    # El decorador es un envoltorio funcional. Le dice a python que la función es un Gestor de Contexto (Context Manager) y tiene dos tiempos, una al arrancar (Antes del yield) y otra al apagar la api (Despues del yield)
async def lifespan(app: FastAPI):

    # --- CÓDIGO AL ARRANCAR EL CONTENEDOR ---

    try:
        init_db() # Crea los esquemas y tablas necesarias.

        # Cargar datos históricos (solo se ejecuta si la tabla está vacía)
        
    except Exception as e:
        print(f"❌ Error inicializando la BD: {e}")
    yield   #Pausa la ejecución de la función para seguir con la aplicación.
            #Se pueden configurar acciones a realizar al apagar la api

# Inicialización de la API
app = FastAPI(
    lifespan=lifespan,
    title="Air Quality Barrier API",
    description="API de aislamiento para proteger el acceso a air_quality_db",
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

@app.post("/tickets/", status_code=201)
async def create_ticket(ticket: TicketCreate):
    """
    Endpoint to insert a new ticket record into the raw.tickets table.
    """
    query = text("""
        INSERT INTO raw.tickets (purchase_date, price, shop)
        VALUES (:purchase_date, :price, :shop)
        RETURNING id_ticket;
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
