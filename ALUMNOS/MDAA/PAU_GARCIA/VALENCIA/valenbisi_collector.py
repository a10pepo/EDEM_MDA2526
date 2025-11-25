import psycopg
import os
import time
import requests

    
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
            INSERT INTO valenbisi_raw (station_id, station_name, latitude, longitude, available_bikes, available_slots, station_status, total_capacity, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); """, (station_id, station_name, coordenate_lat, coordenate_lon, available, free, open_station, total_capacity, last_update))
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
        cursor.execute("""TRUNCATE TABLE valenbisi_raw RESTART IDENTITY""")
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
        timestamp TIMESTAMP NOT NULL
        ); """)
        cursor.close()
        conexion.commit()
    except Exception as e:
        print("Error al crear la tabla:", e)    



## EMPIEZA EL CODIGO PRINCIPAL

print("Conectando a la base de datos")
intentos_conexion = 0
conectado = False
while intentos_conexion < 5 and not conectado:
    try:
        # Conectamos a la base de datos
        conexion = psycopg.connect(os.getenv("DATABASE_URL"))
        if conexion:
            print("Conexión exitosa a la base de datos")
            conectado = True
        cursor = conexion.cursor()
    except Exception as e:
        print("Error al conectar a la base de datos, reintentando...")
        print(e)
        intentos_conexion += 1
        time.sleep(10)
        if intentos_conexion == 5:
            print("No se pudo conectar a la base de datos después de varios intentos.")
            exit(1)
            
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
    time.sleep(300)