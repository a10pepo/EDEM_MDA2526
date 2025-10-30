import os
import time
import psycopg
import requests
from datetime import datetime


url = os.getenv("DATABASE_URL")

if not url:
    raise ValueError("No se encontró la variable DATABASE_URL en el entorno.")


for intento in range(10):
    try:
        connection = psycopg.connect(url)
        print("Base de datos conectada con éxito", flush=True)
        break
    except Exception as e:
        print(f"Intento {intento + 1}/10: No se pudo conectar ({e})", flush=True)
        time.sleep(3)
else:
    raise ConnectionError("No se pudo conectar a la base de datos después de varios intentos")


with connection.cursor() as cur:
    cur.execute("DROP TABLE IF EXISTS ahorcado;")
    connection.commit()
    print("Tabla 'ahorcado' borrada.", flush=True)

    cur.execute("""
        CREATE TABLE ahorcado (
            id SERIAL PRIMARY KEY,
            palabra TEXT NOT NULL,
            letras_acertadas TEXT,
            letras_falladas TEXT,
            intentos INT,
            tiempo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    connection.commit()
    print("Tabla 'ahorcado' creada nuevamente.", flush=True)


letras = [
    "E", "A", "O", "I", "U",
    "S", "R", "N", "L", "D", "T", "C", "M", "P", "B", "G", 
    "V", "Y", "Q", "H", "F", "Z", "J", "Ñ", "X", "W", "K"
]


try:
    with connection.cursor() as cur:
        while True:
            palabra = None
            
            while not palabra:
                try:
                    response = requests.get("https://random-word-api.herokuapp.com/word?number=1")
                    if response.status_code == 200:
                        data = response.json()
                        
                        
                        if data and isinstance(data, list) and len(data) > 0:
                            palabra = data[0]
                        

                        if not palabra:
                            print("Respuesta de API no contiene palabra, reintentando...", flush=True)
                            palabra = None 
                    else:
                        print(f"Error API: código {response.status_code}, reintentando...", flush=True)
                        time.sleep(2)
                except Exception as e:
                    print(f"Error conectando con la API: {e}, reintentando...", flush=True)
                    time.sleep(2)

            palabra = palabra.upper()
            print(f"\nNueva palabra obtenida: {palabra}", flush=True)

            huecos = len(palabra)
            intentos = 0
            letras_acertadas = []
            letras_falladas = []

            for letra in letras:
                intentos += 1
                if letra in palabra:
                    apariciones = palabra.count(letra)
                    huecos -= apariciones
                    letras_acertadas.append(letra)
                else:
                    letras_falladas.append(letra)

                
                cur.execute("""
                    INSERT INTO ahorcado (palabra, letras_acertadas, letras_falladas, intentos, tiempo)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    palabra,
                    ','.join(letras_acertadas),
                    ','.join(letras_falladas),
                    intentos,
                    datetime.now()
                ))
                connection.commit()

                if huecos <= 0:
                    print(f"Palabra '{palabra}' adivinada en {intentos} intentos", flush=True)
                    break

            
            print("Esperando 10 segundos para la siguiente palabra...", flush=True)
            time.sleep(10)
finally:
    connection.close()
    print("Conexión cerrada.", flush=True)
