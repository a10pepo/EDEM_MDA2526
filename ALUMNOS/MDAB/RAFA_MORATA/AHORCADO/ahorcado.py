import requests
import time
import os

palabras = []
# Más comunes
letras = [
    "E","A","O","S","R","N","I","D","L","C",
    "T","U","M","P","B","G","V","Y","Q","H",
    "F","Z","J","Ñ","X","K","W"
]

with open("words.txt", "r", encoding="utf-8") as f:
    for line in f:
        palabras.append(line.strip())



intentos = 0

for palabra in palabras:
    aciertos = 0
    for letra in letras:
        intentos = intentos + 1
        if letra in palabra:
            print(letra, palabra)
            aciertos = aciertos + palabra.count(letra)
        if aciertos == len(palabra):
            break

print(intentos)
print(aciertos)

import os, psycopg
# import os → permite trabajar con variables de entorno del sistema.
# import psycopg → librería oficial para conectarte a PostgreSQL en Python
url = os.getenv("DATABASE_URL")
# Obtiene la variable de entorno llamada "DATABASE_URL".
# Esta variable contiene la cadena de conexión necesaria para acceder a la base de datos.
# Si no existe, url será None y fallará al intentar conectar.
connection = psycopg.connect(url)
# Crea la conexión con PostgreSQL usando la URL obtenida.
# Si la base de datos está lista y los datos son correctos, se conecta sin problemas.
# 'connection' representa la sesión activa con PostgreSQL.
cur = connection.cursor()
# Crea un cursor.
# El cursor es el objeto que permite ejecutar sentencias SQL (SELECT, INSERT, CREATE, etc).
print("BD conectada con éxito")

#API
def obtener_palabra_api():
    url = "https://rae-api.com/api/random"
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        data = respuesta.json()
        return data["word"].upper()
    else:
        print("Error al llamar a la API")
        return None
    
letras = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def resolver_palabra(palabra):
    intentos = 0
    aciertos = 0

    for letra in letras:
        intentos += 1
        if letra in palabra:
            aciertos += palabra.count(letra)
        
        if aciertos == len(palabra):
            break
    
    return intentos, aciertos

while True:
    print("Pidiendo palabra a la API...")
    palabra = obtener_palabra_api()

    if palabra:
        print(f"Palabra obtenida: {palabra}")

        intentos, aciertos = resolver_palabra(palabra)

        print(f"Intentos: {intentos}, Aciertos: {aciertos}")
        print("------------------------")

    time.sleep(10)


