import time
import requests
import psycopg2
import os
from datetime import datetime

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

# URL de la API
API_URL = "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records?limit=500"

def get_db_connection():
    """
    Intenta conectar a la base de datos.
    Si la BD aún no está lista, reintenta cada 5 seg.
    """
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            print("Conexión exitosa a PostgreSQL")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Esperando a la base de datos ({e})")
            time.sleep(5)

def fetch_data():
    """Descarga el JSON desde la API de Valencia."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status() # Lanza error si el código HTTP no es 200
        return response.json()
    except Exception as e:
        print(f"Error descargando datos de la API: {e}")
        return None

def save_to_db(conn, data):
    """Parsea el JSON e inserta los datos en la tabla valenbisi_raw."""
    if not data or 'results' not in data:
        print("No se encontraron resultados en la respuesta de la API")
        return

    cursor = conn.cursor()
    current_time = datetime.now()
    records_inserted = 0

    # Iteramos sobre cada estación recibida
    for item in data['results']:
        try:
            # Extraemos los datos del JSON. Usamos .get() para evitar errores si falta un campo.
            station_id = int(item.get('number'))
            station_name = item.get('address')
            
            position = item.get('position', {})
            latitude = position.get('lat')
            longitude = position.get('lon')
            
            available_bikes = int(item.get('available', 0))
            available_slots = int(item.get('free', 0))
            total_capacity = int(item.get('total', 0))
            
            is_open = item.get('open', True)
            station_status = 'OPEN' if is_open else 'CLOSED'

            # SQL
            query = """
                INSERT INTO valenbisi_raw 
                (station_id, station_name, latitude, longitude, available_bikes, 
                available_slots, station_status, total_capacity, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                station_id, station_name, latitude, longitude, available_bikes,
                available_slots, station_status, total_capacity, current_time
            ))
            records_inserted += 1

        except Exception as e:
            print(f"Error procesando estación ID {item.get('number')}: {e}")
            conn.rollback() # Si falla una, deshacemos para no bloquear todo
            continue

    # Confirmamos los cambios en la base de datos
    conn.commit()
    cursor.close()
    print(f"[{current_time}] 💾 Guardados {records_inserted} registros.")


# BUCLE PRINCIPAL

def main():
    print("Iniciando Valenbisi")
    
    # 1. Conectar a la BD
    conn = get_db_connection()

    # 2. Bucle infinito
    while True:
        print("--- Iniciando ciclo de recolección ---")
        
        data = fetch_data()

        if data:
            save_to_db(conn, data)

        print("Durmiendo 5 minutos")
        time.sleep(300)

if __name__ == "__main__":
    main()