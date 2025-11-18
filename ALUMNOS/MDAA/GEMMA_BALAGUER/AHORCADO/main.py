import psycopg
import unicodedata
import requests
import time
import os
import json #para manejar la respuesta de la API


abecedario = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's',
    't', 'u', 'v', 'w', 'x', 'y', 'z'
]

try:
    connection = psycopg.connect("postgresql://postgres:postgres@db:5432/pruebadb")
    cur = connection.cursor()
    print("BD conectada con éxito")
except Exception as e:
    print(f"Error: No se pudo conectar a la BD - {e}")

def crear_tabla():
    query = """CREATE TABLE IF NOT EXISTS AHORCADO(
            id SERIAL PRIMARY KEY,
            palabra VARCHAR(100) NOT NULL,
            letras_acertadas TEXT NOT NULL,
            letras_falladas TEXT NOT NULL,
            intentos INT NOT NULL,
            register_date TIMESTAMPTZ NOT NULL DEFAULT now()
        );"""
    cur.execute(query)
    connection.commit()
    print("Tabla AHORCADO creada o ya existía")

crear_tabla()

# Resolver ahorcado
total_intentos = 0

def resolver_ahorcado(palabras):
    global total_intentos
    for palabra in palabras:
        palabra_sin_acentos = unicodedata.normalize('NFKD', str(palabra)).encode('ascii', 'ignore').decode('utf-8').lower() #para no obtener la palabra con tildes
        palabra = str(palabra)
        intentos = 0
        aciertos = 0
        letras_acertadas = ""
        letras_falladas = ""

        for letra in abecedario:
            intentos += 1
            if letra in palabra:
                aciertos += palabra.count(letra)
                letras_acertadas += letra
            else:
                letras_falladas += letra

            if aciertos >= len(palabra):
                break

        cur.execute("""
            INSERT INTO AHORCADO (palabra, letras_acertadas, letras_falladas, intentos)
            VALUES (%s, %s, %s, %s)
        """, (palabra, letras_acertadas.upper(), letras_falladas.upper(), intentos))
        connection.commit()

        total_intentos += intentos


def obtener_palabra_aleatoria():
    """
    Realiza una petición al endpoint /api/random de rae-api.com
    y devuelve la palabra si tiene éxito.
    """
    API_URL = "https://rae-api.com/api/random"
    try:
        response = requests.get(API_URL, timeout=10) # Añadir timeout
        response.raise_for_status() # Lanza una excepción para códigos de error 4xx/5xx
        
        data = response.json()
        
        # El endpoint devuelve un JSON con una estructura como: {"ok": true, "data": {"word": "..."}}
        if data.get('ok') and 'word' in data.get('data', {}):
            palabra = data['data']['word']
            print(f"| API: Palabra recibida: **{palabra}**")
            return palabra
        else:
            print("| API: Formato de respuesta no esperado.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"| API: Error al obtener la palabra: {e}")
        return None
    except json.JSONDecodeError:
        print("| API: Error al decodificar la respuesta JSON.")
        return None

# --- Bucle Principal para la FASE 4 ---

def bucle_automatico():
    print("\n--- INICIANDO FASE 4: API ---")
    while True:
        print(f"\n[{time.strftime('%H:%M:%S')}] Pidiendo palabra a la API...")
        
        palabra = obtener_palabra_aleatoria()
        
        if palabra:
            # La función resolver_ahorcado espera una lista de palabras, así que le pasamos [palabra]
            resolver_ahorcado([palabra])
            print(f"| Total de palabras resueltas hasta ahora. Total intentos: {total_intentos}")
        else:
            print("| No se pudo obtener la palabra. Reintentando...")

        print(f"--- Esperando 10 segundos... ---")
        time.sleep(10) # Espera de 10 segundos

# Ejecutar el bucle principal
bucle_automatico()

######En el apartado 4 me salta el error 502 




   