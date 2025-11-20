import os
import psycopg
import requests
import time

connection = None
cur = None 

for intento in range(10):
    try:
        print(f"Intento de conexión {intento + 1}/10")
        #URL CONEXIÓN A BD 
        url = os.getenv("DATABASE_URL")
        #CONEXIÓN A BD
        connection = psycopg.connect(url)
        # Cursor
        cur = connection.cursor()
        print("BD conectada con éxito")
        break
    except Exception as e:
        print(f"Error conectando a la BD: {e}")
        if intento < 9:
            print("Reintentando en 5 segundos...")
            time.sleep(5)
        else:
            print("No se pudo conectar a la BD después de 10 intentos.")

if connection and cur:
    def createIntentos ():
        query = """CREATE TABLE IF NOT EXISTS Intentos(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    palabra TEXT,
    letras_acertadas TEXT,
    letras_falladas TEXT,
    intentos INTEGER,
    tiempo TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );"""
        cur.execute(query)
        print("Tabla creada con exito")
    createIntentos()
    connection.commit()



letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Ñ"]


def ahorcado():
    total=0
    with open("palabras.txt", encoding="utf-8") as texto:
        for line in texto:
            palabra = line.strip().upper()
            intentos = 0
            letras_adivinadas = ''
            letras_falladas = ''
            for letra in letras:
                intentos += 1
                if letra in palabra:
                    letras_adivinadas += letra
                else:
                    letras_falladas += letra
                if all(l in letras_adivinadas for l in palabra):
                    total += intentos
                    break     
                print(f"la palabra {palabra} se adivino en {intentos} intentos.")

                query = """INSERT INTO Intentos (palabra, letras_acertadas, letras_falladas, intentos) 
                VALUES (%s, %s, %s, %s);"""
                cur.execute(query, (palabra, letras_adivinadas, letras_falladas, intentos))
                connection.commit()
    print(f"El total de intentos para todas las palabras: {total}")
ahorcado()

