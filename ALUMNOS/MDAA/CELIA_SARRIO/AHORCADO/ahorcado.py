import os
import sys
import psycopg
import time
from psycopg.errors import OperationalError 
from datetime import datetime

def db_connection():
    """
    Intenta establecer la conexión a la base de datos con try-except y reintentos.
    """
    try:
        url = os.getenv("DATABASE_URL")
        if not url:
            raise ValueError("Variable de entorno DATABASE_URL no configurada.")
        
        max_retries = 10 
        retry_delay = 3 
        
        for attempt in range(max_retries):
            try:
                connection = psycopg.connect(url)
                print("BD conectada con éxito")
                return connection, connection.cursor()
            except OperationalError as e:
                print(f"Intento {attempt + 1}/{max_retries}: BD no lista. Reintentando en {retry_delay} segundos...")
                time.sleep(retry_delay)
            except Exception as e:
                print(f"Error durante la conexión: {e}")
                time.sleep(retry_delay)
        
        raise Exception("Fallo la conexión a la Base de Datos después de varios intentos.")

    except Exception as e:
        print(f"Error fatal: {e}")
        sys.exit(1)

def createIntentos (cur, connection):
    """
    Crea la tabla INTENTOS si no existe.
    """
    query = """CREATE TABLE IF NOT EXISTS INTENTOS (
id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
palabra VARCHAR(100),
letras_acertadas VARCHAR(50),
letras_falladas VARCHAR(50),
intentos INTEGER,
tiempo TIMESTAMPTZ NOT NULL DEFAULT NOW()
);"""
    cur.execute(query)
    connection.commit()
    print("Tabla 'INTENTOS' asegurada.")


# OPTIMIZACIÓN DE FASE 5
# Ordenado por frecuencia en el idioma español
letras = ["E", "A", "O", "S", "R", "N", "I", "L", "D", "C", "T", "U", "M", "P", "B", "G", "V", "Y", "Ñ", "Q", "H", "F", "Z", "J", "X", "W", "K"]



def Ahorcado_Fase5(cur, connection):
    """
    Lógica principal del Ahorcado (Fase 5).
    Lee un archivo de palabras (pasado como argumento) y lo resuelve usando la estrategia de frecuencia de letras optimizada.
    """

    if len(sys.argv) != 2:
        print(f"Uso: python {sys.argv[0]} <archivo_palabras>")
        print("Error: No se proporcionó el archivo de palabras como argumento.")
        sys.exit(1)
        
    archivo_palabras = sys.argv[1]

    total_global = 0
    try:
        with open(archivo_palabras, encoding="utf-8") as texto:
            print(f"Leyendo palabras de {archivo_palabras}...")
            for line in texto:
                palabra = line.strip().upper()
                
                if not palabra:
                    continue

                letras_requeridas = set(c for c in palabra if c.isalpha())
                if not letras_requeridas:
                    continue 

                intentos = 0
                letras_adivinadas = set()
                letras_falladas = set() 

                for letra in letras:
                    if letras_requeridas.issubset(letras_adivinadas):
                        break

                    intentos += 1
                    
                    if letra in palabra:
                        letras_adivinadas.add(letra)
                    else:
                        letras_falladas.add(letra)

                    letras_acertadas_str = "".join(sorted(list(letras_adivinadas)))
                    letras_falladas_str = "".join(sorted(list(letras_falladas)))

                    query = """INSERT INTO INTENTOS (palabra, letras_acertadas, letras_falladas, intentos, tiempo) VALUES (%s, %s, %s, %s, %s);"""
                    cur.execute(query, (palabra, letras_acertadas_str, letras_falladas_str, intentos, datetime.now()))
                    connection.commit()

                if letras_requeridas.issubset(letras_adivinadas):
                    print(f"Palabra '{palabra}' adivinada en {intentos} intentos (Estrategia Optimizada).")
                    total_global += intentos
                else:
                    print(f"Palabra '{palabra}' NO adivinada. (Intentos: {intentos})")

    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_palabras}' no fue encontrado.")
        sys.exit(1)

    print(f"\nTotal de intentos para todas las palabras (Optimizado): {total_global}") 

if __name__ == "__main__":
    print("Iniciando servicio del Ahorcado (Fase 5: Optimización)")
    
    cur = None
    connection = None
    
    try:
        # 1. Conectar a la BD
        connection, cur = db_connection()
        
        if cur and connection:
            # 2. Asegurar la tabla
            createIntentos(cur, connection)
            
            # 3. Iniciar la lógica de la Fase 5 (que lee el archivo)
            Ahorcado_Fase5(cur, connection)
            
        else:
            print("Error crítico: No se pudo conectar a la base de datos. Saliendo.")
            sys.exit(1)
            
    except (Exception, KeyboardInterrupt) as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"¡ERROR INESPERADO!: {e}")
        print("El script ha fallado.")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        import traceback
        traceback.print_exc()
        
    finally:
        # Asegurarse de cerrar la conexión si se abrió
        if cur:
            cur.close()
        if connection:
            connection.close()
        print("Cerrando conexión y finalizando script.")
