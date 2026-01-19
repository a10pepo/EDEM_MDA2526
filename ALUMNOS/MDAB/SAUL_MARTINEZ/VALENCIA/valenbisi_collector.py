import requests
import psycopg2
import time
import schedule
import os
from datetime import datetime
from pymongo import MongoClient

# Configuración postgres
DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'valenbisi_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')
# tanto en user como password funciona aunque yo le ponga user y password diferentes en el .env 
# pero solo porque está en docker y coge directamente la info dentro del DB_USER por prioridad, 
# si no encontrara la variable DB_USER ya se iría al "user" que había escrito
# URL de la API (Aumentamos el limit a 100 para tener una muestra significativa)

# Configuración de Mongo
MONGO_URL = "mongodb://mongo:27017/" # Conectamos al servicio mongo de Docker

API_URL = "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records?limit=100"

def get_db_connection():
    """Conexión a postgres con reintentos."""
    while True:
        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
            return conn
        except psycopg2.OperationalError as e:
            print(f"Base de datos postgres no lista ({e}). Reintentando en 5s...")
            time.sleep(5)
        
def get_mongo_collection():
    """Conexión a MongoDB."""
    try:
        client = MongoClient(MONGO_URL)
        db = client["valenbisi_nosql"] # Base de datos
        collection = db["stations_raw"] # Colección (equivalente a tabla)
        return collection
    except Exception as e:
        print(f"Error conectando a Mongo: {e}")
        return None

def init_db():
    """Crea la tabla SQL al inicio y asegura el commit."""
    print("--- Verificando esquema de Base de Datos SQL---")
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
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
        """)
        conn.commit() # IMPORTANTE: Guardar el cambio de estructura
        print("Tabla 'valenbisi_raw' verificada/creada exitosamente.")
        cur.close()
    except Exception as e:
        print(f"Error creando tabla: {e}")
        conn.rollback()
    finally:
        conn.close()

def fetch_and_store_data():
    print(f"[{datetime.now()}] Iniciando ciclo de recolección...") #Tanto de SQL como de NoSQL
    
    # 1. Obtener datos de la API
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error contactando API: {e}")
        return
    
    records = data.get('results', [])
    current_time = datetime.now()

    # 2. Guardar en Base de Datos
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        records = data.get('results', [])
        
        for item in records:
            try:
                geo = item.get('geo_point_2d', {})

                cur.execute("""
                    INSERT INTO valenbisi_raw 
                    (station_id, station_name, latitude, longitude, available_bikes, available_slots, station_status, total_capacity, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    int(item.get('number', 0)),
                    item.get('address', 'Unknown'),
                    geo.get('lat', 0.0),
                    geo.get('lon', 0.0),
                    int(item.get('available', 0)),
                    int(item.get('free', 0)),
                    item.get('status', 'Unknown'),
                    int(item.get('total', 0)),
                    datetime.now()
                ))
            except Exception as row_error:
                print(f"Error saltando fila defectuosa: {row_error}")
                # No hacemos rollback aquí para intentar salvar las otras filas, 
                # pero en inserciones masivas (batch) es mejor rollback.
        
        conn.commit() # Guardamos todos los datos insertados
        print(f"--- Éxito: {len(records)} registros procesados ---")
        cur.close()

    except Exception as e:
        print(f"Error en transacción de base de datos: {e}")
        conn.rollback() # IMPORTANTE: Limpia el error para la próxima vez
    finally:
        conn.close()

# 3. Guardar en MongoDB (NoSQL)
    mongo_coll = get_mongo_collection()
    if mongo_coll is not None:
        try:
            # En NoSQL podemos guardar el JSON casi directo.
            # Añadimos el timestamp nosotros para saber cuándo lo guardamos.
            documents_to_insert = []
            for item in records:
                doc = item.copy() # Copiamos el dato de la API
                doc['ingested_at'] = current_time # Le ponemos nuestra fecha
                documents_to_insert.append(doc)
            
            if documents_to_insert:
                mongo_coll.insert_many(documents_to_insert)
                print(f"--- NoSQL: {len(documents_to_insert)} documentos guardados en Mongo ---")
        except Exception as e:
            print(f"Error insertando en Mongo: {e}")

if __name__ == "__main__":
    # Esperamos unos segundos extra para asegurar que Postgres arrancó del todo
    time.sleep(5)
    init_db()
    
    # Primera ejecución inmediata
    fetch_and_store_data()
    
    # Programar
    schedule.every(5).minutes.do(fetch_and_store_data)
    
    while True:
        schedule.run_pending()
        time.sleep(1)