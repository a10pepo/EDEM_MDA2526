import os
import time
import psycopg
import requests
from datetime import datetime

# Leer la URL de conexión
url = os.getenv("DATABASE_URL")

if not url:
    raise ValueError("No se encontró la variable DATABASE_URL en el entorno.")

# Esperar a que la BD esté lista
for intento in range(10):
    try:
        connection = psycopg.connect(url)
        print("Base de datos conectada con éxito")
        break
    except Exception as e:
        print(f"Intento {intento + 1}/10: No se pudo conectar ({e})")
        time.sleep(3)
else:
    raise ConnectionError("No se pudo conectar a la base de datos después de varios intentos")

# Crear cursor y tabla
with connection.cursor() as cur:
    
    print("Tabla 'ahorcado' borrada.")

    # Crear tabla de nuevo
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
    print("Tabla 'ahorcado' creada nuevamente.")

# Variables del juego
letras = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", 
    "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", 
    "U", "V", "W", "X", "Y", "Z"
]

# Cargar palabras
palabras = []
try:
    with open("palabras.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            palabras.append(linea.strip().upper())
    print(f"{len(palabras)} palabras cargadas desde palabras.txt")
except FileNotFoundError:
    print("No se encontró el archivo 'palabras.txt'.")
    palabras = ["PRUEBA"]

# Simulación del juego: una fila por cada intento
with connection.cursor() as cur:
    for palabra in palabras:
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

            # Insertar fila por cada intento
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
                print(f"Palabra '{palabra}' adivinada en {intentos} intentos")
                break

connection.close()
print("Proceso completado y conexión cerrada.")
