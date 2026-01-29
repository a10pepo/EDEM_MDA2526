import os
import sys
import psycopg
from datetime import datetime
import requests
import time

# PASO 1: CONECTARNOS A LA BASE DE DATOS
url = os.getenv("DATABASE_URL")
connection = psycopg.connect(url)
cur = connection.cursor()
print("BD conectada con éxito")

# PASO 2: CONECTARNOS A LA API
def conectar_api():
    url = "https://rae-api.com/api/random"
    try:
        response = requests.get(url)
        data = response.json()
        print(data)
        return data
    except:
        print(f"Error")

# PASO 3: LA PALABRA TIENE QUE ESTAR EN MAYÚSCULAS Y SIN TILDES
def limpiar_palabra(palabra):
    palabra = palabra.upper()
    palabra = palabra.replace("Á","A").replace("É","E").replace("Í","I").replace("Ó","O").replace("Ú","U")
    return palabra

# PASO 4: CREAR LA TABLA PARA GUARDAR LOS DATOS
def createTableAhorcado():
    try:
        query = """
        CREATE TABLE IF NOT EXISTS ahorcado_sinIA_API (
            id SERIAL PRIMARY KEY,
            palabra VARCHAR(255) NOT NULL,
            letras_acertadas VARCHAR(100),
            letras_fallidas VARCHAR(100),
            intentos INTEGER NOT NULL,
            tiempo TIMESTAMP NOT NULL
        );
        """
        cur.execute(query)
        connection.commit()
        print("Tabla ahorcado creada")
    except Exception as e:
        print("Error creando la tabla ahorcado", e)
createTableAhorcado()


# # PASO 5: BUCLE + INSERTAR RESULTADOS + OPTIMIZACION: colocamos las letras del abecedario de más o menos comunes
abecedario = ["E","A","O","S","R","N","I","D","L","C","T","U","M","P","B","G","V","Y","Q","H","F","Z","J","Ñ","X","K","W"]

while True:
    data = conectar_api()
    palabra = limpiar_palabra(data["data"]["word"])
    letras_acertadas = []
    letras_fallidas = []
    intentos = 0

    for letra_a in abecedario:
        intentos += 1
        for letra_l in palabra:
            if letra_a == letra_l and letra_a not in letras_acertadas:
                letras_acertadas.append(letra_a)
        if letra_a not in palabra and letra_a not in letras_fallidas:
            letras_fallidas.append(letra_a)
        
        letras_acertadas_str = "".join(sorted(letras_acertadas))
        letras_fallidas_str = "".join(sorted(letras_fallidas))
        cur.execute(
            "INSERT INTO ahorcado_sinIA_API (palabra, letras_acertadas, letras_fallidas, intentos, tiempo) VALUES (%s, %s, %s, %s, %s)",
            (palabra, letras_acertadas_str, letras_fallidas_str, intentos, datetime.now())
        )
        connection.commit()
        
        if len(letras_acertadas) == len(set(palabra)):
            print(f"Palabra: {palabra}; Intentos: {intentos}")
            break

    time.sleep(10)  