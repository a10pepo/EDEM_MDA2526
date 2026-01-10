import os
from funciones import f_conexion_bd, f_llamada_api


API_URL = "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records?limit=20"
DATABASE_URL = os.getenv("DATABASE_URL")


#CONEXIÓN A BD con intentos y tiempo de espera

connection = f_conexion_bd(DATABASE_URL,"valenbisi_db")

# Cursor.
# Crea un cursor, que es un objeto que permite ejecutar comandos SQL.
# - El cursor es como un "canal" entre tu código y la base de datos: puedes enviar consultas (SELECT, INSERT, etc.) y recibir resultados.
cur = connection.cursor()
print("Cursor creado con éxito")

#=============================================#
#=========== CREACIÓN TABLA ==================#
#=============================================#

cur.execute("""
                CREATE TABLE valenbisi_raw (
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

connection.commit()

response = f_llamada_api(API_URL,"valenbisi_api")
data = response.json()
print(data)

try:
    # 1. Extraemos la lista de estaciones
    # 'response' es el diccionario que te devolvió f_llamada_api
    estaciones = data.get('results', [])
    
    print(f"Comenzando la carga de {len(estaciones)} estaciones...")

    # 2. Preparamos la consulta SQL
    query_insert = """
        INSERT INTO valenbisi_raw (
            station_id, station_name, latitude, longitude, 
            available_bikes, available_slots, station_status, 
            total_capacity, timestamp
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for st in estaciones:
        # 3. Transformación: Extraemos los campos necesarios
        # Usamos .get() para evitar errores si falta alguna clave
        station_id = st.get('number')
        station_name = st.get('address')
        
        # Las coordenadas están dentro del sub-objeto geo_point_2d
        geo = st.get('geo_point_2d', {})
        lat = geo.get('lat')
        lon = geo.get('lon')
        
        bikes = st.get('available')
        slots = st.get('free')
        status = st.get('open')
        total = st.get('total')
        time_data = st.get('update_jcd')

        # 4. Ejecución del insert
        cur.execute(query_insert, (
            station_id, station_name, lat, lon,
            bikes, slots, status, total, time_data
        ))

    # 5. Confirmamos la transacción
    connection.commit()
    print("✅ Carga masiva completada con éxito en PostgreSQL.")

except Exception as e:
    print(f"❌ Error durante la inserción: {e}")
    connection.rollback()
finally:
    cur.close()
    connection.close()