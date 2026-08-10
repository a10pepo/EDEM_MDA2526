import time
import os
import logging
import requests
import psycopg2
from datetime import datetime
from psycopg2.extras import execute_values

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Variables de entorno
API_URL = "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records"
DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'valenbisi_db')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

# SQL
SQL_CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS valenbisi_raw (
        id SERIAL PRIMARY KEY,
        station_id INTEGER NOT NULL,
        station_name VARCHAR(255),
        latitude DECIMAL(10, 8),
        longitude DECIMAL(11, 8),
        available_bikes INTEGER,
        available_slots INTEGER,
        station_status VARCHAR(50),
        total_capacity INTEGER,
        timestamp TIMESTAMP NOT NULL
    );
"""

SQL_INSERT = """
    INSERT INTO valenbisi_raw 
    (station_id, station_name, latitude, longitude, available_bikes, available_slots, station_status, total_capacity, timestamp)
    VALUES %s
"""


def get_db_connection():
    """Crea una conexión a la base de datos."""
    try:
        return psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
    except Exception as e:
        logging.error(f"Error conectando a la BD: {e}")
        return None

def init_db():
    """Crea la tabla si no existe al iniciar el script"""
    conn = get_db_connection()
    if not conn: return
    
    try:
        with conn.cursor() as cur:
            cur.execute(SQL_CREATE_TABLE)
            conn.commit()
        logging.info("Base de datos inicializada correctamente.")
    except Exception as e:
        logging.error(f"Error creando tabla: {e}")
    finally:
        conn.close()

# Extract
def extract_data_from_api():
    """Descarga TODOS los datos de la API de Valenbisi con paginación"""
    all_records = []
    limit = 100
    offset = 0
    
    logging.info("Conectando a la API de Valenbisi...")
    
    while True:
        try:
            url = f"{API_URL}?limit={limit}&offset={offset}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            batch = data.get("results", [])
            
            if not batch:
                break
                
            all_records.extend(batch)
            
            # Si recibimos menos registros que el límite, hemos llegado al final
            if len(batch) < limit:
                break
                
            offset += limit
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error en la API: {e}")
            return [] # Retornamos lista vacía si falla para no romper el programa
            
    logging.info(f"Descargados {len(all_records)} registros crudos")
    return all_records

# Transform
def transform_data(raw_records):
    """Limpia y organiza los datos para la base de datos"""
    clean_data = []
    query_time = datetime.now()

    for item in raw_records:
        # Extraer geo
        geo = item.get('geo_point_2d', {})
        
        # Normalizar estado (Open/Closed)
        is_open = item.get('open') # Puede venir como boolean o string "T"/"F"
        status = "OPEN" if is_open == "T" or is_open is True else "CLOSED"

        # Crear tupla ordenada para SQL
        record = (
            item.get('number'),                  # station_id
            item.get('address'),                 # station_name
            geo.get('lat'),                      # latitude
            geo.get('lon'),                      # longitude
            int(item.get('available', 0)),       # available_bikes
            int(item.get('free', 0)),            # available_slots
            status,                              # station_status
            int(item.get('total', 0)),           # total_capacity
            query_time                           # timestamp
        )
        clean_data.append(record)
        
    return clean_data

# Load
def load_data_to_db(data):
    """Inserta los datos limpios en PostgreSQL."""
    if not data:
        logging.warning("No hay datos para guardar")
        return

    conn = get_db_connection()
    if not conn: return

    try:
        with conn.cursor() as cur:
            # execute_values es muy eficiente para insertar listas grandes
            execute_values(cur, SQL_INSERT, data)
            conn.commit()
            logging.info(f"Guardados {len(data)} registros en BD")
    except Exception as e:
        logging.error(f"Error insertando datos: {e}")
    finally:
        conn.close()


def main():
    logging.info("Iniciando Valenbisi Collector (ETL)...")
    
    # 1. Preparar BD (solo una vez al principio)
    init_db()
    
    # 2. Bucle infinito
    while True:
        logging.info("Iniciando ciclo de recolección")
        
        # Paso 1: Extract
        raw_data = extract_data_from_api()
        
        if raw_data:
            # Paso 2: Transform
            processed_data = transform_data(raw_data)
            
            # Paso 3: Load
            load_data_to_db(processed_data)
        
        logging.info("Durmiendo 5 minutos")
        time.sleep(300)

if __name__ == "__main__":
    main()