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