import psycopg 
import os as os
from datetime import datetime
import requests as requests 

#Leemos las variables de entorno del contenedor en curso (definidas en el composer)
HOST = os.getenv("POSTGRES_HOST", "localhost")
NAME = os.getenv("POSTGRES_DB", "ahorcado_db")
USER = os.getenv("POSTGRES_USER", "alvarogc")
PASSWORD = os.getenv("POSTGRES_PASSWORD", "hola123")

#Creamos la conexión cazando las variables de entorno
connection = psycopg.connect(
        host=HOST,
        dbname=NAME,
        user=USER,
        password=PASSWORD
    )

#Creamos el cursor para poder interactuar con la base de datos y la creamos
cur = connection.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS resultados (
    palabra VARCHAR(50),
    letras_acertadas VARCHAR(50),
    letras_falladas VARCHAR(50),
    intentos INT,
    tiempo TIMESTAMP
)
""")
connection.commit()

#Tomamos las palabras del fichero de texto
lista_palabras = []
with open("palabras.txt", mode="r", encoding="utf-8") as file:
    for line in file:
        lista_palabras.append(line.rstrip('\n'))

print(lista_palabras)

#Generamos el diccionario de letras e inicializamos contador de intentos, ordenamos por probabilidad en castellano
diccionario_letras = ["e","a","o","l","s","n","d","r","u","i","t","c","p","m","y","q","b","h","g","f","v","j","ñ","z","x","w","k"]
contador_intentos = 0 

#Iteramos sobre todas las palabras
for palabra in lista_palabras: 
    
    palabra_sin_duplicados = set(palabra.lower())  # letras únicas en minúscula
    letras_acertadas = ""       #almacenará las letras descubiertas
    letras_falladas = ""        #almacenará las letras incorrectas
    intentos = 0                #contador local de intentos

    #Simulamos probar letra por letra del alfabeto
    for letra in diccionario_letras:
        intentos += 1
        contador_intentos += 1  #Cada prueba cuenta como intento, para todas las palabras
        
        if letra in palabra_sin_duplicados:
            letras_acertadas += letra
        else: 
            letras_falladas += letra

        #Ya hemos encontrado todas las letras, salimos del bucle
        if len(letras_acertadas) == len(palabra_sin_duplicados):
            break

    #Insertamos el resultado final de la palabra en la base de datos
    cur.execute("""
        INSERT INTO resultados (palabra, letras_acertadas, letras_falladas, intentos, tiempo)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        palabra.upper(),
        letras_acertadas.upper(),
        letras_falladas.upper(),
        intentos,
        datetime.now()
    ))
    connection.commit()

#MOSTRAMOS TODOS LOS RESULTADOS
print("RESULTADOS INSERTADOS EN LA BASE DE DATOS:")

cur.execute("SELECT * FROM resultados")
registros = cur.fetchall()

for fila in registros:
    print(fila)

#Cerramos la conexión con la base de datos
cur.close()
connection.close()

#Ahora hacemos la petición a la API para que traiga una palabra random
response = requests.get("https://rae-api.com/api/random")
palabra = response.json()
print(palabra["data"]["word"])

# Inicializamos variables
palabra_sin_duplicados = set(palabra["data"]["word"].lower())
letras_acertadas = ""
letras_falladas = ""
intentos = 0
contador_intentos = 0

# Simulamos probar letra por letra del alfabeto
for letra in diccionario_letras:
    intentos += 1
    contador_intentos += 1

    if letra in palabra_sin_duplicados:
        letras_acertadas += letra
    else: 
        letras_falladas += letra

    # Ya hemos encontrado todas las letras, salimos del bucle
    if len(letras_acertadas) == len(palabra_sin_duplicados):
        break

print(contador_intentos)