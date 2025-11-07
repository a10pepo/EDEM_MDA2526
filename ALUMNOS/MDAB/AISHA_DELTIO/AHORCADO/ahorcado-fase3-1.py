import string
import os
import sys
import psycopg
import datetime

ABECEDARIO = string.ascii_uppercase

def crear_tabla(cursor):

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ahorcado (
        id SERIAL PRIMARY KEY,
        palabra VARCHAR(255) NOT NULL,
        letras_acertadas VARCHAR(100),
        letras_fallidas VARCHAR(100),
        intentos INTEGER NOT NULL,
        tiempo TIMESTAMP NOT NULL
    );
    """)
    print("Tabla 'ahorcado' asegurada.")

def procesar_e_insertar_palabras(connection, cursor, lista_de_palabras):
    sql_insert = """
    INSERT INTO ahorcado 
        (palabra, letras_acertadas, letras_fallidas, intentos, tiempo)
    VALUES (%s, %s, %s, %s, %s);
    """
    total_insertadas = 0
    
    for linea in lista_de_palabras:
        palabra = linea
        if not palabra:
            continue
            
        letras_objetivo = set(palabra)
        letras_acertadas = set()
        letras_fallidas = set()
        
        print(f"--- Procesando: {palabra} ---")
        
        for i, letra in enumerate(ABECEDARIO, 1):
            intentos = i 
            if letra in letras_objetivo:
                letras_acertadas.add(letra)
            else:
                letras_fallidas.add(letra)

            try:
                datos_intento_actual = (
                    palabra,
                    "".join(sorted(letras_acertadas)),  
                    "".join(sorted(letras_fallidas)), 
                    intentos,
                    datetime.datetime.now() 
                )
                
                cursor.execute(sql_insert, datos_intento_actual)
                connection.commit()
                
                print(f"  > Intento {intentos} ({letra}) para '{palabra}' insertado.")
                total_insertadas += 1

            except Exception as e:
                print(f"ERROR insertando intento {intentos} para '{palabra}': {e}")
                connection.rollback()
                break 
            if letras_acertadas == letras_objetivo:
                print(f"  > Palabra '{palabra}' completada.")
                break # Dejamos de procesar esta palabra
    
    print(f"\nProceso completado. Se insertaron {total_insertadas} registros (intentos).")


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Uso: python ahorcado.py <fichero_palabras>")
        sys.exit(1)
    fichero = sys.argv[1]
    url = os.getenv("DATABASE_URL")

    # --- Bloque principal de ejecución ---
    conn = None
    try:
        with psycopg.connect(url) as conn:
            print("BD conectada con éxito.")
            
            with conn.cursor() as cur:
                
                # --- Paso A: Crear la tabla ---
                crear_tabla(cur)
                conn.commit() 

                # --- Paso B: Leer fichero completo ---
                print("Leyendo fichero de palabras...")
                try:
                    with open(fichero, 'r', encoding='utf-8') as f:
                        lista_de_palabras = f.readlines() # Leemos las líneas
                except FileNotFoundError:
                    print(f"Error: El fichero '{fichero}' no se encontró.")
                    sys.exit(1)
                
                # --- Paso C: Procesar e insertar palabras ---
                procesar_e_insertar_palabras(conn, cur, lista_de_palabras)

        print("\n--- Proceso completado ---")

    except Exception as e:
        print(f"Error fatal: {e}")
        if conn:
            conn.rollback() # Revertir la transacción completa si algo falló
        sys.exit(1)
    finally:
        if conn:
            conn.close()
            print("Conexión cerrada.")