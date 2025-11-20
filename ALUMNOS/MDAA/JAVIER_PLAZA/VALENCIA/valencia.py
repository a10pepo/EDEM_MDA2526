import requests 
import psycopg
import os
import time

respuesta = requests.get("https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records?limit=20")

respuesta = respuesta.json()


def crear_tabla():
    try:
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
        ); """) 
        connection.commit()
    except Exception as e:
        print("Error al crear la tabla:", e)

def añadirDatos(station_id, station_name, latitude, longitude, available_bikes, available_slots, station_status, total_capacity, timestamp):
    try:
        query = """INSERT INTO valenbisi_raw(station_id, station_name, latitude, longitude, available_bikes, available_slots, station_status, total_capacity, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cur.execute(query, (station_id, station_name, latitude, longitude, available_bikes, available_slots, station_status, total_capacity, timestamp))
        connection.commit()
        print('Datos añadidos')
    except Exception as e:
        print("Error:", e)

try: 
    url = os.getenv("DATABASE_URL")
    connection = psycopg.connect(url)
    cur = connection.cursor()
    print('Base de datos conectada con exito')
except Exception as e:
    print('Error', e)

crear_tabla()

# for resultado in respuesta["results"]:
#     for station_id in resultado["number"]:
#         for station_name in resultado["address"]:
#             for latitude in resultado["geo_point_2d"]["lat"]:
#                 for longitude in resultado["geo_point_2d"]["lon"]:
#                     for available_bikes in resultado["available"]:
#                         for available_slots in resultado["free"]:
#                             for station_status in resultado["open"]:
#                                 for total_capacity in resultado["total"]:
#                                     for timestamp in resultado["update_jcd"]:
#                                         añadirDatos(station_id, station_name, latitude, longitude, available_bikes, available_slots, station_status, total_capacity, timestamp)

for resultado in respuesta["results"]:
    station_id = resultado["number"]
    station_name = resultado["address"]
    latitude = resultado["geo_point_2d"]["lat"]
    longitude = resultado["geo_point_2d"]["lon"]
    available_bikes = resultado["available"]
    available_slots = resultado["free"]
    station_status = resultado["open"]
    total_capacity = resultado["total"]
    timestamp = resultado["update_jcd"]
    añadirDatos(station_id, station_name, latitude, longitude, available_bikes, available_slots, station_status, total_capacity, timestamp)