import os
import psycopg
from datetime import datetime
import requests
import time

url = os.getenv("DATABASE_URL")
print(url)
    #CONEXIÓN A BD
try:
    connection = psycopg.connect(url)
    cur = connection.cursor()
    print('BD CONECTADA')
except Exception as e:
    print(f"Error fatal al conectar a la BD: {e}")
    exit()



query = """CREATE TABLE IF NOT EXISTS partidas_ahorcado (
    palabra VARCHAR(100) NOT NULL ,
    letras_acertadas VARCHAR(100),
    letras_falladas VARCHAR(100),
    intentos INT NOT NULL DEFAULT 0,
    tiempo TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);"""

cur.execute(query)
connection.commit()
print('Tabla creada')


letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']



palabras=[]
with open("palabras.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        palabras.append(linea.strip().upper())

api_url = "https://random-word-api.herokuapp.com/word?number=1"
intentos=0

            
print('Iniciando bucle', flush=True)

try:
    while True:
        palabra_api = ""
        palabra_normalizada = ""
        
        try:
            response = requests.get(api_url)
            data = response.json()
            palabra_api = data[0]

            palabra_normalizada = palabra_api.strip().upper()

        except requests.exceptions.RequestException as e:
            print(f"Error al contactar la API: {e}. Reintentando en 10s.", flush=True)
            time.sleep(10)
            continue # inicio del while True

        # resolver

        letras_acertadas = ''
        letras_falladas = ''

        huecos = len(palabra_normalizada)


        for letra in letras:

            if huecos == 0:
                break

            intentos += 1
            timestamp = datetime.now()
            
            query_insert = """INSERT into partidas_ahorcado(
                    palabra, letras_acertadas, letras_falladas, intentos, tiempo)
                    VALUES (%s, %s, %s, %s, %s);"""

            if letra in palabra_normalizada:

                acierto = palabra_normalizada.count(letra)
                huecos -= acierto
                letras_acertadas += letra
            
            else:
                letras_falladas += letra

            values = (
                palabra_normalizada, 
                letras_acertadas,
                letras_falladas,
                intentos,
                timestamp
            )
            
            try:
                cur.execute(query_insert, values)
                connection.commit()
            except Exception as e:
                print(f"Error al insertar en BD: {e}")
                connection.rollback()
        print(f"¡Palabra '{palabra_normalizada}' resuelta! Intentos totales acumulados: {intentos}", flush=True)
        print("Esperando 10 segundos para la siguiente palabra...", flush=True)
        time.sleep(10)

except KeyboardInterrupt:
    print("\nProceso detenido por el usuario.", flush=True)
finally:
    if 'connection' in locals() and not connection.closed:
        cur.close()
        connection.close()
        print("Conexión a BD cerrada.", flush=True)
