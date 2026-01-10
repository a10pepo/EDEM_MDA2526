import requests
import time
import psycopg2
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "valenbisi_db")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password123")

# URL base (sin el límite, lo añadiremos dinámicamente)
BASE_URL = "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records"

def esperar_base_datos():
    while True:
        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
            conn.close()
            print("¡Conexión exitosa a la Base de Datos!")
            break
        except psycopg2.OperationalError:
            print("Esperando a que la base de datos esté lista...")
            time.sleep(3)

def crear_tabla():
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS valenbisi_raw (
                id SERIAL PRIMARY KEY,
                station_id INTEGER,
                station_name VARCHAR(255),
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                available_bikes INTEGER,
                available_slots INTEGER,
                station_status VARCHAR(50),
                total_capacity INTEGER,
                timestamp TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Tabla 'valenbisi_raw' verificada.")
    except Exception as e:
        print(f"Error al crear tabla: {e}")

def obtener_todas_estaciones():
    """Descarga todas las estaciones usando paginación"""
    todas_estaciones = []
    offset = 0
    limit = 100 # El máximo permitido por la API suele ser 100
    
    while True:
        try:
            url = f"{BASE_URL}?limit={limit}&offset={offset}"
            response = requests.get(url).json()
            
            # Verificar si la API devolvió un error
            if 'error_code' in response:
                print(f"⚠️ ERROR API: {response.get('message')}")
                break
                
            resultados = response.get('results', [])
            
            if not resultados:
                break # No hay más datos, salimos del bucle
                
            todas_estaciones.extend(resultados)
            
            # Si bajamos menos de 100, es que ya hemos llegado al final
            if len(resultados) < limit:
                break
                
            offset += limit # Preparamos el siguiente bloque
            
        except Exception as e:
            print(f"Error de conexión con la API: {e}")
            break
            
    return todas_estaciones

def guardar_datos():
    try:
        # 1. Obtener datos con paginación
        estaciones = obtener_todas_estaciones()
        
        if not estaciones:
            print("[ALERTA] No se han encontrado estaciones. Revisa la URL o la conexión.")
            return

        ahora = datetime.now()

        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()

        query = """
            INSERT INTO valenbisi_raw 
            (station_id, station_name, latitude, longitude, available_bikes, available_slots, station_status, total_capacity, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        datos_insertar = []
        for est in estaciones:
            geo = est.get('geo_point_2d', {})
            lat = geo.get('lat')
            lon = geo.get('lon')
            
            bicis = est.get('available', 0)
            huecos = est.get('free', 0)
            total = est.get('total', bicis + huecos)
            
            status_raw = est.get('open')
            status = 'OPEN' if status_raw == 'T' or status_raw == True else 'CLOSED'

            fila = (
                est.get('number'),
                est.get('address'),
                lat,
                lon,
                bicis,
                huecos,
                status,
                total,
                ahora
            )
            datos_insertar.append(fila)

        cur.executemany(query, datos_insertar)
        conn.commit()
        print(f"[{ahora}] INSERT realizado (API Oficial): {len(datos_insertar)} estaciones guardadas.")
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error en el ciclo de guardado: {e}")

if __name__ == "__main__":
    print("--- Iniciando Valenbisi Collector (API v2.1 Paginada) ---")
    esperar_base_datos()
    crear_tabla()
    
    while True:
        guardar_datos()
        time.sleep(300) # 5 minutos