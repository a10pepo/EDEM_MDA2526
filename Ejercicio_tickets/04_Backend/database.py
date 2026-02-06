from sqlalchemy import text, types
from config_env import engine # Importamos el engine centralizado
import time
import pandas as pd
import os
from pathlib import Path

def init_db():
    """Inicializa la infraestructura de la base de datos (esquemas, tablas y vistas)."""
    for i in range(10):
        try:
            # Usamos engine.connect() y manejamos la transacción manualmente
            with engine.connect() as conn:
                print(f"Intento {i+1}: Conectado con SQLAlchemy. Configurando esquemas...")
                
                # 1. Creación de esquemas
                conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))

                # 2. Tabla de registro de tickets (datos de la API)
                # NOTA: Pongo "import" entre comillas dobles porque es palabra reservada en SQL
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS raw.tickets (
                        ticket_id           INT PRIMARY KEY,
                        timestamp       TIMESTAMPTZ NOT NULL,
                        address VARCHAR,
                        shop_name VARCHAR,
                        latitud NUMERIC(9,6),
                        longitud NUMERIC(9,6),
                        product_name VARCHAR,
                        "import" NUMERIC(10,2), 
                        refund_deadline TIMESTAMPTZ,
                        change_deadline TIMESTAMPTZ
                    );
                """))

                # ------------------------------------------------------------------
                # 3. NUEVA TABLA: DICCIONARIO DE CATEGORÍAS
                # Esta tabla sustituye al CSV (seed) que íbamos a usar en dbt
                # ------------------------------------------------------------------
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS raw.categories (
                        product_name VARCHAR PRIMARY KEY,
                        category VARCHAR
                    );
                """))

                # ------------------------------------------------------------------
                # 4. POBLAR EL DICCIONARIO
                # Insertamos las categorías fijas.
                # ON CONFLICT DO NOTHING evita errores si reinicias el contenedor.
                # ------------------------------------------------------------------
                conn.execute(text("""
                    INSERT INTO raw.categories (product_name, category)
                    VALUES 
                        ('Producto A', 'Tecnología'),
                        ('Producto B', 'Tecnología'),
                        ('Producto C', 'Alimentación'),
                        ('Producto D', 'Ocio'),
                        ('Producto E', 'Ropa')
                    ON CONFLICT (product_name) DO NOTHING;
                """))

                # ------------------------------------------------------------------
                # 5. CREAR LA VISTA FINAL (EL "DBT" INTEGRADO)
                # Esta vista hace el JOIN automático. 
                # Desde visualización consultarás 'public.ventas_finales', NO 'raw.tickets'.
                # ------------------------------------------------------------------
                conn.execute(text("""
                    CREATE OR REPLACE VIEW public.ventas_finales AS
                    SELECT 
                        t.ticket_id,
                        t.timestamp,
                        t.shop_name,
                        t.address as address,       -- Corregimos typo
                        t.latitud as latitude,     -- Traducimos a inglés
                        t.longitud as longitude,   -- Traducimos a inglés
                        t.product_name,
                        t."import" as amount,      -- Renombramos 'import' a 'amount'
                        
                        -- Lógica de negocio: Cruzamos con la tabla de categorías
                        COALESCE(c.category, 'Sin Categoría') as category,
                        
                        t.refund_deadline,
                        t.change_deadline
                    FROM raw.tickets t
                    LEFT JOIN raw.categories c ON t.product_name = c.product_name;
                """))

                conn.commit()
                print("✅ Base de datos lista: Tickets, Categorías y Vista Final creadas.")
                return 

        except Exception as e:
            print(f"⚠️ Intento {i+1} fallido: {e}")
            time.sleep(2)

    raise RuntimeError("No se pudo conectar a la base de datos tras 10 intentos.")