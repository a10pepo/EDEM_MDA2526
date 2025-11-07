import string
import os
import sys
import psycopg
import datetime
import requests
import json
import time
import unicodedata

# El abecedario (sin 'Ñ' ni tildes) que usaremos para simular
ABECEDARIO = string.ascii_uppercase

def get_random_word():
    """Obtener una palabra aleatoria de la RAE API."""
    try:
        url = "https://rae-api.com/api/random"
        headers = {"Accept": "application/json"}
        # Añadimos un timeout para evitar que se quede colgado
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Lanza error si la respuesta es 4xx o 5xx
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error de red o API: {e}")
        return None

def normalizar_palabra(palabra):
    """
    Limpia la palabra:
    1. Descompone tildes (NFD): "á" -> "a" + "´"
    2. Filtra caracteres no espaciados (Mn): "a" + "´" -> "a"
    3. Pasa a mayúsculas.
    4. Filtra cualquier cosa que no esté en nuestro ABECEDARIO.
    """
    s = unicodedata.normalize('NFD', palabra)
    s_sin_tildes = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s_limpia = "".join(c for c in s_sin_tildes.upper() if c in ABECEDARIO)
    return s_limpia

def crear_tabla(cursor):
    """Asegura que la tabla 'ahorcado2' exista en la BD."""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ahorcado2 (
        id SERIAL PRIMARY KEY,
        palabra VARCHAR(255) NOT NULL,
        letras_acertadas VARCHAR(100),
        letras_fallidas VARCHAR(100),
        intentos INTEGER NOT NULL,
        tiempo TIMESTAMP NOT NULL
    );
    """)
    print("Tabla 'ahorcado' asegurada.")

def procesar_una_palabra(palabra_limpia):
    """
    Simula el juego para UNA sola palabra y devuelve una lista 
    con todos los pasos de la simulación.
    """
    registros_palabra = []
    
    # La palabra ya viene limpia y en mayúsculas de normalizar_palabra()
    if not palabra_limpia:
        return []
            
    print(f"--- Procesando palabra: {palabra_limpia} ---")
    
    letras_objetivo = set(palabra_limpia)
    letras_acertadas = set()
    letras_fallidas = set()
    
    # Iteramos por el abecedario para simular los intentos
    for i, letra in enumerate(ABECEDARIO, 1):
        intentos = i
        
        if letra in letras_objetivo:
            letras_acertadas.add(letra)
        else:
            letras_fallidas.add(letra)

        # Añadimos la tupla de datos (el estado actual)
        registros_palabra.append((
            palabra_limpia,
            "".join(sorted(letras_acertadas)),
            "".join(sorted(letras_fallidas)),
            intentos,
            datetime.datetime.now()
        ))

        # Si ya encontramos todas, paramos de simular ESTA palabra
        if letras_acertadas == letras_objetivo:
            print(f"Palabra '{palabra_limpia}' resuelta en {intentos} intentos.")
            break
    
    return registros_palabra

def guardar_datos(cursor, registros_de_una_palabra):
    """Guarda la lista de registros de una simulación en la BD."""
    if not registros_de_una_palabra:
        print("No se generaron registros para esta palabra.")
        return

    sql_insert = """
    INSERT INTO ahorcado2 
        (palabra, letras_acertadas, letras_fallidas, intentos, tiempo)
    VALUES (%s, %s, %s, %s, %s);
    """
    
    print(f"Guardando {len(registros_de_una_palabra)} registros en la BD...")
    # executemany es eficiente para insertar múltiples filas
    cursor.executemany(sql_insert, registros_de_una_palabra)


if __name__ == "__main__":
    
    url = os.getenv("DATABASE_URL")
    if not url:
        print("Error: La variable de entorno DATABASE_URL no está definida.")
        sys.exit(1)

    conn = None
    try:
        # Usamos 'with' para asegurar que la conexión se gestione correctamente
        with psycopg.connect(url) as conn:
            print("BD conectada con éxito.")
            
            # 1. Crear la tabla UNA SOLA VEZ al inicio
            with conn.cursor() as cur_setup:
                crear_tabla(cur_setup)
                conn.commit() 

            # 2. Bucle infinito para procesar palabras
            while True:
                palabra_guardada = False
                try:
                    # --- Paso A: Obtener palabra de la API ---
                    resultado_api = get_random_word()
                    
                    if not (resultado_api and resultado_api.get("ok")):
                        print("No se pudo obtener palabra de la API. Reintentando...")
                        palabra_guardada = False # Marcamos para no imprimir éxito
                    
                    else:
                        palabra_original = resultado_api["data"]["word"]
                        
                        # --- Paso B: Limpiar y normalizar la palabra ---
                        palabra_norm = normalizar_palabra(palabra_original)

                        if not palabra_norm:
                            print(f"Palabra original '{palabra_original}' no contiene letras válidas. Saltando.")
                            palabra_guardada = False
                        else:
                            # --- Paso C: Procesar la palabra ---
                            registros = procesar_una_palabra(palabra_norm)

                            # --- Paso D: Guardar en BD (si hay registros) ---
                            if registros:
                                with conn.cursor() as cur_juego:
                                    guardar_datos(cur_juego, registros)
                                # Hacemos commit DESPUÉS de guardar CADA palabra
                                conn.commit() 
                                print(f"¡Palabra '{palabra_norm}' guardada con éxito!")
                                palabra_guardada = True

                except Exception as e_loop:
                    # Captura error en el procesamiento de UNA palabra
                    # (ej. API falla, etc.) pero no mata el script.
                    print(f"Error en el ciclo de juego (palabra saltada): {e_loop}")
                    if conn:
                        conn.rollback() # Revertir la transacción de esta palabra
                
                # --- Paso E: Esperar 10 segundos ---
                if palabra_guardada:
                    print(f"\n--- Esperando 10 segundos para la siguiente palabra... (Ctrl+C para salir) ---")
                else:
                    print(f"\n--- Hubo un problema, reintentando en 10 segundos... (Ctrl+C para salir) ---")
                
                time.sleep(10)

    except (KeyboardInterrupt, SystemExit):
        # Permite salir limpiamente con Ctrl+C
        print("\nProceso interrumpido por el usuario. Cerrando conexión.")
    except Exception as e:
        print(f"Error fatal fuera del bucle: {e}")
        if conn:
            conn.rollback() # Revertir la transacción completa si algo falló
    finally:
        # Esto se ejecuta siempre, asegurando que la conexión se cierre
        if conn:
            conn.close()
            print("Conexión cerrada.")