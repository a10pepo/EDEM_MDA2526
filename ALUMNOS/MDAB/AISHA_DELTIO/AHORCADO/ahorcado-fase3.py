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

def procesar_palabras(lista_de_palabras):
    registros_totales = []
    
    for linea in lista_de_palabras:
        palabra = linea
        if not palabra:
            continue
        
        print(f"--- Procesando: {palabra} ---")
        
        letras_objetivo = set(palabra)
        letras_acertadas = set()
        letras_fallidas = set()
        
        # Iteramos por el abecedario para ESTA palabra
        for i, letra in enumerate(ABECEDARIO, 1):
            intentos = i
            
            if letra in letras_objetivo:
                letras_acertadas.add(letra)
            else:
                letras_fallidas.add(letra)

            # Añadimos la tupla de datos a la lista TOTAL
            registros_totales.append((
                palabra,
                "".join(sorted(letras_acertadas)),
                "".join(sorted(letras_fallidas)),
                intentos,
                datetime.datetime.now()
            ))

            # Si ya encontramos todas, paramos de simular ESTA palabra
            if letras_acertadas == letras_objetivo:
                break
    
    # Devolvemos la lista gigante con todo
    return registros_totales

def guardar_datos(cursor, registros_totales):
    if not registros_totales:
        print("No se generaron registros para guardar.")
        return

    sql_insert = """
    INSERT INTO ahorcado 
        (palabra, letras_acertadas, letras_fallidas, intentos, tiempo)
    VALUES (%s, %s, %s, %s, %s);
    """
    
    print(f"\nGuardando {len(registros_totales)} registros en la BD (esto puede tardar)...")
    cursor.executemany(sql_insert, registros_totales)


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Uso: python ahorcado.py <fichero_palabras>")
        sys.exit(1)
    fichero = sys.argv[1]
    url = os.getenv("DATABASE_URL")

    # --- Bloque principal de ejecución ---
    conn = None
    try:
        # Usamos 'with' para asegurar que la conexión se cierre sola
        with psycopg.connect(url) as conn:
            print("BD conectada con éxito.")
            
            with conn.cursor() as cur:
                
                # --- Paso A: Crear la tabla ---
                crear_tabla(cur)
                conn.commit() 

                # --- Paso B: Leer fichero completo ---
                print("Leyendo fichero de palabras...")
                with open(fichero, 'r', encoding='utf-8') as f:
                    lista_de_palabras = f.readlines() 
                
                # --- Paso C: Procesar la lista completa ---
                registros = procesar_palabras(lista_de_palabras)

                # --- Paso D: Guardar el lote completo ---
                if registros:
                    guardar_datos(cur, registros)
                    conn.commit() # Un solo commit para TODAS las palabras
                    print("¡Datos guardados con éxito!")
                else:
                    print("No se encontraron palabras válidas en el fichero.")

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
            

