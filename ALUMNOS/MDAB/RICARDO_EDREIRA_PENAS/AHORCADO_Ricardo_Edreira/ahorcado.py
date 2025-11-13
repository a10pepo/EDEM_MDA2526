import os, psycopg
from datetime import datetime
import time
#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")

cur.execute("""CREATE TABLE IF NOT EXISTS resultados 
        (id SERIAL PRIMARY KEY,
        palabra VARCHAR(50),
        letras_acertadas VARCHAR(255),
        letras_falladas VARCHAR(255),
        intentos INT,
        tiempo TIMESTAMP)""")
connection.commit()

letras = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
intentos_maximos = 206

palabras = set()
try:
    with open("palabras.txt", encoding="utf-8") as f:
        for line in f:
            w = line.strip().upper()
            if w: 
                palabras.add(w)
except FileNotFoundError:
    print("Error: Asegúrate de que 'palabras.txt' existe en el directorio.")
    exit()

intentos = 0
for palabra in palabras:
    aciertos = 0
    for letra in letras:
        intentos=intentos+1
        if letra in palabra:
            print(letra,palabra)
            aciertos = aciertos + palabra.count(letra)  
        if aciertos == len(palabra):
            break
    print(intentos)
    print(aciertos)
    tiempo_actual = datetime.now()              
    cur.execute("INSERT INTO resultados (palabra, letras_acertadas, letras_falladas, intentos, tiempo) VALUES (%s, %s, %s, %s, %s)",
            (palabra, ''.join([l for l in letras if l in palabra]), 
            ''.join([l for l in letras if l not in palabra]), 
            intentos, tiempo_actual))
    connection.commit()
    intentos = 0

# Cerrar cursor y conexión
cur.close()
connection.close()