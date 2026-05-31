import os, psycopg, time
from datetime import datetime

url = os.getenv("DATABASE_URL")

for intento in range(10):
    try:
        connection = psycopg.connect(url)
        print("BD conectada con éxito")
        break
    except Exception as e:
        print(f"Esperando BD... ({intento + 1}/10): {e}")
        time.sleep(3)
else:
    print("No se pudo conectar a la BD.")
    exit(1)

cur = connection.cursor()

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