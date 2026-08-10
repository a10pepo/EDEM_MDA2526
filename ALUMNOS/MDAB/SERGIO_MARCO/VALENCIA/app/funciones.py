import psycopg, requests, time

def f_conexion_bd(db_url, db_nombre):
    for i in range(10):
        try:            
            connection = psycopg.connect(db_url)
            print(f"BD {db_nombre} conectada con éxito")
            return connection
        
        except psycopg.OperationalError as e:
            print(f"Intento {i+1}: la BD {db_nombre} aún no está lista. Esperando...")
            time.sleep(2)
    raise RuntimeError(f"No se pudo conectar a la BD {db_nombre} tras 10 intentos")


def f_llamada_api(api_url, api_nombre): #Establece la conexión a una API. Devuelve el json de respuesta.
    for i in range(10):
        try:
            
            response = requests.get(api_url)
            # print(f"API {api_nombre} conectada con éxito")
            return response
        
        except requests.exceptions.RequestException as e:
            print(f"Intento {i+1}: la API {api_nombre} aún no está lista. Esperando...")
            time.sleep(2)
    raise RuntimeError(f"No se pudo conectar a la API {api_nombre} tras 10 intentos")


def f_run_ingestion(database_url, api_url):

    connection = f_conexion_bd(database_url,"valenbisi_db")
    cur = connection.cursor()
    response = f_llamada_api(api_url,"valenbisi_api")
    data = response.json()

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

        for estacion in estaciones:
            # 3. Transformación: Extraemos los campos necesarios
            # Usamos .get() para evitar errores si falta alguna clave
            station_id = estacion.get('number')
            station_name = estacion.get('address')
            
            # Las coordenadas están dentro del sub-objeto geo_point_2d
            geo = estacion.get('geo_point_2d', {})
            lat = geo.get('lat')
            lon = geo.get('lon')
            
            bikes = estacion.get('available')
            slots = estacion.get('free')
            status = estacion.get('open')
            total = estacion.get('total')
            time_data = estacion.get('update_jcd')

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