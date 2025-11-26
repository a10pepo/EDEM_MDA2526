import psycopg
import os
import time
import requests
import datetime

    
def insert_data(conexion,data):
    results = data["results"]
    for station in results:
        station_id = station["number"]
        station_name = station["address"]
        coordenate_lon = station["geo_point_2d"]["lon"]
        coordenate_lat = station["geo_point_2d"]["lat"]
        available = station["available"]
        free = station["free"]
        open_station = station["open"]
        last_update = station["update_jcd"]
        total_capacity = station["total"]
        print(station_id, station_name, coordenate_lon, coordenate_lat, available, free, open_station, last_update)
        try:
            cursor = conexion.cursor()
            cursor.execute("""
            INSERT INTO valenbisi_raw (station_id, station_name, latitude, longitude, available_bikes, available_slots, station_status, total_capacity, last_update, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """, (station_id, station_name, coordenate_lat, coordenate_lon, available, free, open_station, total_capacity, last_update, datetime.datetime.now()))
            cursor.close()
            conexion.commit()
            print(f"insertado con exito estación n {station_id}")
        except Exception as e:
            print("Error al insertar", e)
            exit[1]
        
def get_data_bicis(offset, limit):
    try:
        url = f"https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records?limit={limit}&offset={offset}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def crear_tabla(conexion):
    try:
        cursor = conexion.cursor()
        # cursor.execute("""DROP TABLE valenbisi_raw CASCADE""")
        cursor.execute("""
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
        last_update TIMESTAMP NOT NULL,
        timestamp TIMESTAMP NOT NULL
        ); """)
        cursor.close()
        conexion.commit()
    except Exception as e:
        print("Error al crear la tabla:", e)    



## EMPIEZA EL CODIGO PRINCIPAL

# Configuración de la conexión directa
DB_USER = "postgres"
DB_PASS = "postgres"
DB_HOST = "db_valenbisi"      # nombre del contenedor
DB_PORT = "5432"    # dentro de docker
DB_NAME = "valenbisi_db"

SERVER_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/postgres"
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ====================================
# CREAR BASE DE DATOS SI NO EXISTE
# ====================================
def create_database_if_not_exists():
    print(f"Verificando base '{DB_NAME}'...")

    try:
        with psycopg.connect(SERVER_URL) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
                exists = cur.fetchone()

                if not exists:
                    print(f"No existe. Creando '{DB_NAME}'...")
                    cur.execute(f"CREATE DATABASE {DB_NAME};")
                    print("Base creada correctamente.")
                else:
                    print("La base ya existe.")
    except Exception as e:
        print(f"Error creando/verificando base: {e}")
        exit(1)

def ensure_database():
    for _ in range(10):  # intenta 10 veces
        try:
            print("Verificando base '%s'...", DB_NAME)
            conn = psycopg.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASS,
                dbname="postgres"  # se conecta a postgres para crear la BD
            )
            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
            exists = cur.fetchone()

            if not exists:
                print("Base no existe. Creándola...")
                cur.execute(f"CREATE DATABASE {DB_NAME};")
            else:
                print("La base ya existe.")

            cur.close()
            conn.close()
            return
        except Exception as e:
            print("Error creando/verificando base: %s", e)
            time.sleep(3)

    raise Exception("Postgres no respondió después de varios intentos")

# Intentos de conexión
intentos_conexion = 0
conectado = False
while intentos_conexion < 5 and not conectado:
    try:
        conexion = psycopg.connect(DB_URL)
        conectado = True
        print("Conexión exitosa a la base de datos")
    except Exception as e:
        intentos_conexion += 1
        print(f"Error al conectar (intento {intentos_conexion}/5): {e}")
        time.sleep(5)

if not conectado:
    print("No se pudo conectar a la base de datos.")
    exit(1)

create_database_if_not_exists()
ensure_database()           
crear_tabla(conexion)
while True:
    offset = 0
    limit = 100
    while True:
        data = get_data_bicis(offset,limit)
        if len(data["results"])>0:
            insert_data(conexion,data)
            offset += limit
        else:
            break
    time.sleep(600)