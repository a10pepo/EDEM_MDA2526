#tener un programa con las siguientes características:Lea las palabras de un fichero de texto, una por línea 
# Busque cada palabra y retorne los intentos necesarios para adivinarla

import os
import psycopg #(no entiendo porque no lo toma)
from datetime import datetime

#aca defino el abcdario para q el bot lo usepara adivinar -por fuerza bruta)
letras = ["A","B","C","D","E","F","G","H","I","J", "K", "L", "M", "N","O", "P", "Q", "R", "S", "T","U","V", "W", "X", "Y", "Z"]

#esto lee las palabra sy las guarda en un set)
palabras = set()
with open("palabras.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            palabras.add(w)

print("palabras cargadas:" , palabras)


#FASE2+3
#aca es donde conecto a esta base de dtos (yo la tenia aparte en un "main.py" porqueeee?) 


url = os.getenv("DATABASE_URL")
connection = psycopg.connect(url)
cur = connection.cursor()
print("BD conectada con éxito")


# Crear tabla si no existe
def crear_tabla():
    query = """CREATE TABLE IF NOT EXISTS basededatos(
        id SERIAL PRIMARY KEY,
        palabra VARCHAR(100) NOT NULL,
        letras_acertadas VARCHAR(100),
        letras_falladas VARCHAR(100),
        intentos NUMERIC,
        tiempo TIMESTAMPTZ NOT NULL DEFAULT NOW());"""
    cur.execute(query)
    connection.commit()
    print("tabla creada")

crear_tabla()

# Simulación del juego y registro de resultados
for palabra in palabras:
    letras_acertadas = ""
    letras_falladas = ""
    intentos = 0

    for letra in letras:
        intentos += 1
        if letra in palabra:
            letras_acertadas += letra
        else:
            letras_falladas += letra

        if len(letras_acertadas) == len(set(palabra)):
            print(f"✅ '{palabra}' adivinada en {intentos} intentos.")
            break

    # Registrar resultado para esta palabra
    cur.execute("""INSERT INTO basededatos (palabra, letras_acertadas, letras_falladas, intentos, tiempo)
    VALUES (%s, %s, %s, %s, %s);""", (palabra, letras_acertadas, letras_falladas, intentos, datetime.now()))
    connection.commit()

cur.close()
connection.close()
print("fin del juego")


