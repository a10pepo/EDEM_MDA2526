from sqlalchemy import text, types
from config import engine # Importamos el engine centralizado
import time
import pandas as pd
import os
from pathlib import Path


def init_db():
    """Inicializa la infraestructura de la base de datos (esquemas y tablas)."""
    for i in range(10):
        try:
            # Usamos engine.connect() y manejamos la transacción manualmente
            with engine.connect() as conn:
                print(f"Intento {i+1}: Conectado con SQLAlchemy. Configurando esquemas...")
                
                # 1. Creación de esquemas (Capas de Medallón)
                # Es obligatorio usar text() para ejecutar strings en SQLAlchemy

                conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
                # conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging;"))
                # conn.execute(text("CREATE SCHEMA IF NOT EXISTS intermediate;"))
                # conn.execute(text("CREATE SCHEMA IF NOT EXISTS marts;"))

                # 2. Tabla de registro de tickets (datos de la API)
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS raw.tickets (
                        ticket_id          INT PRIMARY KEY,
                        timestamp       TIMESTAMPTZ NOT NULL,
                        adress VARCHAR,
                        shop_name VARCHAR,
                        latitud NUMERIC(9,6),
                        longitud NUMERIC(9,6),
                        product_name VARCHAR,
                        import NUMERIC(10,2), -- Renamed from 'price' to match the dict key
                        refund_deadline TIMESTAMPTZ,
                        change_deadline TIMESTAMPTZ
                    );
                """))
                conn.commit()
                print("✅ Base de datos lista: Esquemas y tablas RAW creados correctamente.")
                return

        except Exception as e:
            print(f"⚠️ Intento {i+1} fallido: {e}")
            time.sleep(2)

    raise RuntimeError("No se pudo conectar a la base de datos tras 10 intentos.")


