import sys
import string
import os
import psycopg2
from datetime import datetime
from time import sleep

def connect_to_db():
    for _ in range(15): 
        try:
            conn = psycopg2.connect(
                host=os.environ.get("DB_HOST", "db"),
                database=os.environ.get("DB_NAME", "ahorcado_db"),
                user=os.environ.get("DB_USER", "user"),
                password=os.environ.get("DB_PASSWORD", "password")
            )
            return conn
        except psycopg2.OperationalError:
            print("Esperando a la base de datos...")
            sleep(1)
    raise ConnectionError("No se pudo conectar a la base de datos.")

def setup_db(conn):
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS resultados;") 
        cur.execute("""
            CREATE TABLE resultados (
                id SERIAL PRIMARY KEY,
                palabra VARCHAR(50) NOT NULL,
                letras_acertadas VARCHAR(26) NOT NULL,
                letras_falladas VARCHAR(26) NOT NULL,
                intentos INTEGER NOT NULL,
                tiempo TIMESTAMP WITHOUT TIME ZONE NOT NULL
            );
        """)
    conn.commit()
    conn.commit()

def adivinar_palabra_por_fuerza_bruta_y_log(conn, palabra_objetivo):
    
    palabra_upper = palabra_objetivo.upper()
    palabra_limpia = palabra_objetivo.lower()
    
    letras_a_descubrir = set(char for char in palabra_limpia if 'a' <= char <= 'z')
    
    letras_acertadas_set = set()
    letras_falladas_set = set()
    
    intentos = 0

    with conn.cursor() as cur:
        for letra in string.ascii_lowercase:
            
            intentos += 1
            
            if letra in palabra_limpia:
                letras_acertadas_set.add(letra)
            else:
                letras_falladas_set.add(letra)

            acertadas_str = "".join(sorted(list(letras_acertadas_set)))
            falladas_str = "".join(sorted(list(letras_falladas_set)))
            
            cur.execute("""
                INSERT INTO resultados (palabra, letras_acertadas, letras_falladas, intentos, tiempo)
                VALUES (%s, %s, %s, %s, %s);
            """, (palabra_upper, acertadas_str, falladas_str, intentos, datetime.now()))
            
            conn.commit()
            
            if letras_acertadas_set == letras_a_descubrir:
                print(f"| Palabra: {palabra_upper.ljust(15)} | Intentos loggeados: {intentos}")
                return
def print_results(conn):
    print("CONTENIDO FINAL DE LA TABLA RESULTADOS")
    

    sql_query = """
        SELECT palabra, intentos, letras_acertadas, tiempo 
        FROM resultados 
        ORDER BY palabra, intentos 
        LIMIT 206;
    """
    
    with conn.cursor() as cur:
        cur.execute(sql_query)
        rows = cur.fetchall()
        
        print(f"{'Palabra'.ljust(15)} | {'Intentos'.ljust(10)} | {'Aciertos'.ljust(15)} | {'Tiempo'}")
        print("-" * 65)
        
        for row in rows:
            palabra, intentos, acertadas, tiempo = row
            
            print(f"{palabra.ljust(15)} | {str(intentos).ljust(10)} | {acertadas.ljust(15)} | {tiempo}")
def ejecutar_ahorcado_db(lista_palabras):
    
    conn = connect_to_db()
    setup_db(conn)
    print("Conexión y tabla 'resultados' creadas.")

    print("Iniciando Simulación y Log de Datos")
    for palabra in lista_palabras:
        if not palabra:
            continue
        adivinar_palabra_por_fuerza_bruta_y_log(conn, palabra.strip())

    print_results(conn) 

    conn.close()
    print(" Proceso completado. Datos almacenados y mostrados.")


if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Uso: python ahorcado.py palabras.txt")
        sys.exit(1)
    
    nombre_archivo = sys.argv[1]
    
    try:
        with open(nombre_archivo, "r") as f:
            lista_palabras = [linea.strip() for linea in f if linea.strip()]
    except Exception as e:
        print(f"Error al leer {nombre_archivo}: {e}")
        sys.exit(1)

    if not lista_palabras:
        print(f"El archivo {nombre_archivo} está vacío o no contiene palabras válidas :(")
        sys.exit(1)
        
    ejecutar_ahorcado_db(lista_palabras)