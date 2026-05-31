import os
import time
import string
import psycopg
from datetime import datetime
import requests

# Verificación del archivo
ruta_archivo = os.path.join(os.path.dirname(__file__), "palabras.txt")
if not os.path.exists(ruta_archivo):
    print(f"⚠️ No se encontró el archivo: {ruta_archivo}")
    exit(1)

conjunto_palabras = []
with open(ruta_archivo, encoding="utf-8") as archivo:
    for linea in archivo:
        palabra_original = linea.strip()
        if palabra_original:
            conjunto_palabras.append(palabra_original.lower())


# Configuración alfabeto
ALFABETO = list("abcdefghijklmnñopqrstuvwxyz")
ABECEDARIO = string.ascii_lowercase + "ñ"


# Funciones
def normalizar_palabra(palabra):
    return palabra.strip().lower().replace(" ", "")

def concatenar_elementos(elementos):
    return "".join(elementos)

def fuerza_bruta(palabras, alfabeto):
    registros_totales = []
    for palabra in palabras:
        intentos_en_palabra = 0
        letras_acertadas = []
        letras_falladas = []
        letras_requeridas = set(palabra)
        for letra in alfabeto:
            if not letras_requeridas:
                break
            intentos_en_palabra += 1
            if letra in palabra:
                letras_acertadas.append(letra.upper())
                letras_requeridas.remove(letra)
            else:
                letras_falladas.append(letra.upper())
            registros_totales.append({
                "palabra": palabra.upper(),
                "letras_acertadas": concatenar_elementos(letras_acertadas),
                "letras_falladas": concatenar_elementos(letras_falladas),
                "intentos": intentos_en_palabra,
                "tiempo": datetime.now()
            })
    return registros_totales


# Esperar a PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
for i in range(10):
    try:
        connection = psycopg.connect(DATABASE_URL)
        print("✅ Conectado a PostgreSQL")
        break
    except psycopg.OperationalError:
        print("⏳ PostgreSQL no listo, esperando 3 segundos...")
        time.sleep(3)
else:
    print("❌ No se pudo conectar a PostgreSQL después de varios intentos")
    exit(1)

cur = connection.cursor()

# Tablas y funciones DB
def createTable():
    try:
        query = """
        CREATE TABLE IF NOT EXISTS palabras(
            id SERIAL PRIMARY KEY,
            palabra TEXT,
            letras_acertadas TEXT,
            letras_falladas TEXT,
            intentos INTEGER,
            tiempo TIMESTAMP
        );
        """
        cur.execute(query)
    except Exception as e:
        print("Error al crear tabla:", e)

def insertPalabras(resultados):
    try:
        for resultado in resultados:
            query = """
            INSERT INTO palabras (
                palabra, letras_acertadas, letras_falladas, intentos, tiempo
            ) VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                resultado["palabra"],
                resultado["letras_acertadas"],
                resultado["letras_falladas"],
                resultado["intentos"],
                resultado["tiempo"]
            )
            cur.execute(query, values)
    except Exception as e:
        print("Error al insertar palabras:", e)

def getPalabras():
    cur.execute("SELECT * FROM palabras;")
    print(cur.fetchall())

def deletePalabras():
    cur.execute("TRUNCATE palabras;")


# Lógica principal
createTable()
deletePalabras()

# is_api = os.environ.get("is_api")
# if is_api:
#     while True:
#         try:
#             response = requests.get("https://rae-api.com/api/random")
#             print("dataaaa", response)
#             data = response.json()
#             palabra_api = [data['data']['word']]
#             resultados = fuerza_bruta(palabra_api, ABECEDARIO)
#             insertPalabras(resultados)
#             getPalabras()
#             connection.commit()
#             time.sleep(10)
#         except Exception as e:
#             print("Error API:", e)
# else:
resultados = fuerza_bruta(conjunto_palabras, ABECEDARIO)
insertPalabras(resultados)
connection.commit()

getPalabras()
# Cerrar conexión
cur.close()
connection.close()
print("✅ Script terminado correctamente")
