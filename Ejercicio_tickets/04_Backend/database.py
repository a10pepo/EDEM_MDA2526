from sqlalchemy import text, types
from config import engine # Importamos el engine centralizado
import time
import pandas as pd
import os
from pathlib import Path

# Diccionario con los metadatos de cada estación (basado en la API de Valencia)
# La clave es el objectid (nombre del archivo CSV)

# STATIONS_METADATA = {
#     12: {
#         "nombre": "Dr. Lluch",
#         "direccion": "DR.LLUCH",
#         "tipozona": "Urbana",
#         "tipoemisio": "Tráfico",
#         "fiwareid": "A08_DR_LLUCH_60m",
#         "geo_shape": {"type": "Feature", "geometry": {"coordinates": [-0.328289489402739, 39.4666847554611], "type": "Point"}, "properties": {}},
#         "geo_point_2d": {"lon": -0.328289489402739, "lat": 39.4666847554611}
#     },
#     13: {
#         "nombre": "Francia",
#         "direccion": "AVDA.FRANCIA",
#         "tipozona": "Urbana",
#         "tipoemisio": "Tráfico",
#         "fiwareid": "A01_AVFRANCIA_60m",
#         "geo_shape": {"type": "Feature", "geometry": {"coordinates": [-0.342986232422652, 39.4578268875183], "type": "Point"}, "properties": {}},
#         "geo_point_2d": {"lon": -0.342986232422652, "lat": 39.4578268875183}
#     },
#     14: {
#         "nombre": "Boulevar Sur",
#         "direccion": "BULEVARD SUD",
#         "tipozona": "Urbana",
#         "tipoemisio": "Tráfico",
#         "fiwareid": "A02_BULEVARDSUD_60m",
#         "geo_shape": {"type": "Feature", "geometry": {"coordinates": [-0.396337564375856, 39.4503960055054], "type": "Point"}, "properties": {}},
#         "geo_point_2d": {"lon": -0.396337564375856, "lat": 39.4503960055054}
#     },
#     15: {
#         "nombre": "Molí del Sol",
#         "direccion": "MOLÍ DEL SOL",
#         "tipozona": "Suburbana",
#         "tipoemisio": "Tráfico",
#         "fiwareid": "A03_MOLISOL_60m",
#         "geo_shape": {"type": "Feature", "geometry": {"coordinates": [-0.408809896900938, 39.4811121109041], "type": "Point"}, "properties": {}},
#         "geo_point_2d": {"lon": -0.408809896900938, "lat": 39.4811121109041}
#     },
#     16: {
#         "nombre": "Pista de Silla",
#         "direccion": "PISTA DE SILLA",
#         "tipozona": "Urbana",
#         "tipoemisio": "Tráfico",
#         "fiwareid": "A04_PISTASILLA_60m",
#         "geo_shape": {"type": "Feature", "geometry": {"coordinates": [-0.376643936579157, 39.4580609536967], "type": "Point"}, "properties": {}},
#         "geo_point_2d": {"lon": -0.376643936579157, "lat": 39.4580609536967}
#     },
#     17: {
#         "nombre": "Universidad Politécnica",
#         "direccion": "POLITÈCNIC",
#         "tipozona": "Suburbana",
#         "tipoemisio": "Fondo",
#         "fiwareid": "A05_POLITECNIC_60m",
#         "geo_shape": {"type": "Feature", "geometry": {"coordinates": [-0.337400660521869, 39.4796444969292], "type": "Point"}, "properties": {}},
#         "geo_point_2d": {"lon": -0.337400660521869, "lat": 39.4796444969292}
#     },
#     18: {
#         "nombre": "Viveros",
#         "direccion": "VIVERS",
#         "tipozona": "Urbana",
#         "tipoemisio": "Fondo",
#         "fiwareid": "A06_VIVERS_60m",
#         "geo_shape": {"type": "Feature", "geometry": {"coordinates": [-0.36964822314381, 39.4796409248053], "type": "Point"}, "properties": {}},
#         "geo_point_2d": {"lon": -0.36964822314381, "lat": 39.4796409248053}
#     },
#     19: {
#         "nombre": "Centro",
#         "direccion": "VALÈNCIA CENTRE",
#         "tipozona": "Urbana",
#         "tipoemisio": "Tráfico",
#         "fiwareid": "A07_VALENCIACENTRE_60m",
#         "geo_shape": {"type": "Feature", "geometry": {"coordinates": [-0.376397651655324, 39.4705476702601], "type": "Point"}, "properties": {}},
#         "geo_point_2d": {"lon": -0.376397651655324, "lat": 39.4705476702601}
#     },
#     20: {
#         "nombre": "Cabanyal",
#         "direccion": "CABANYAL",
#         "tipozona": "Urbana",
#         "tipoemisio": "Fondo",
#         "fiwareid": "A09_CABANYAL_60m",
#         "geo_shape": {"type": "Feature", "geometry": {"coordinates": [-0.328534813492744, 39.4743907853568], "type": "Point"}, "properties": {}},
#         "geo_point_2d": {"lon": -0.328534813492744, "lat": 39.4743907853568}
#     },
#     21: {
#         "nombre": "Olivereta",
#         "direccion": "OLIVERETA",
#         "tipozona": "Urbana",
#         "tipoemisio": "Tráfico",
#         "fiwareid": "A10_OLIVERETA_60m",
#         "geo_shape": {"type": "Feature", "geometry": {"coordinates": [-0.405923445529068, 39.469244235092], "type": "Point"}, "properties": {}},
#         "geo_point_2d": {"lon": -0.405923445529068, "lat": 39.469244235092}
#     },
#     22: {
#         "nombre": "Patraix",
#         "direccion": "PATRAIX",
#         "tipozona": "Urbana",
#         "tipoemisio": "Tráfico",
#         "fiwareid": "A11_PATRAIX_60m",
#         "geo_shape": {"type": "Feature", "geometry": {"coordinates": [-0.401411329219129, 39.4591890899964], "type": "Point"}, "properties": {}},
#         "geo_point_2d": {"lon": -0.401411329219129, "lat": 39.4591890899964}
#     },
# }

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

                # 2. Tabla para Valencia (datos en tiempo real de la API)
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS raw.tickets (
                        id_ticket SERIAL PRIMARY KEY,
                        purchase_date TIMESTAMPTZ,
                        price NUMERIC(10,2),
                        shop VARCHAR,
                        UNIQUE(id_ticket)
                    );
                """))
                conn.commit()
                print("✅ Base de datos lista: Esquemas y tablas RAW creados correctamente.")
                return 

        except Exception as e:
            print(f"⚠️ Intento {i+1} fallido: {e}")
            time.sleep(2)

    raise RuntimeError("No se pudo conectar a la base de datos tras 10 intentos.")


