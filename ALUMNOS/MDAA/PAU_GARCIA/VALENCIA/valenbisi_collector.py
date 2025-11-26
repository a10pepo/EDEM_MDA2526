import psycopg
import time
import requests
import datetime

DB_USER = "postgres"
DB_PASS = "postgres"
DB_HOST = "db_valenbisi"
DB_PORT = "5432"
DB_NAME = "valenbisi_db"

SERVER_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/postgres"
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def create_database_if_not_exists():
    try:
        with psycopg.connect(SERVER_URL, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_database WHERE datname=%s;", (DB_NAME,))
                if not cur.fetchone():
                    print(f"Base '{DB_NAME}' no existe. Creando...")
                    cur.execute(f"CREATE DATABASE {DB_NAME};")
                    print("Base creada correctamente.")
                else:
                    print(f"Base '{DB_NAME}' ya existe.")
    except Exception as e:
        print(f"Error al crear/verificar base: {e}")
        exit(1)

def crear_tabla(conexion):
    try:
        with conexion.cursor() as cursor:
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
            );
            """)
        conexion.commit()
    except Exception as e:
        print("Error al crear la tabla:", e)
        exit(1)

# --- Datos API ---
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



# --- EJECUCIÓN ---
create_database_if_not_exists()

# Intentos de conexión a la DB final
for i in range(5):
    try:
        conexion = psycopg.connect(DB_URL)
        print("Conexión exitosa a valenbisi_db")
        break
    except Exception as e:
        print(f"Error al conectar (intento {i+1}/5): {e}")
        time.sleep(5)
else:
    print("No se pudo conectar a la base de datos final.")
    exit(1)

crear_tabla(conexion)

# Loop principal
while True:
    offset = 0
    limit = 100
    while True:
        data = get_data_bicis(offset, limit)
        if data and len(data["results"]) > 0:
            insert_data(conexion, data)
            offset += limit
        else:
            break
    time.sleep(600)
