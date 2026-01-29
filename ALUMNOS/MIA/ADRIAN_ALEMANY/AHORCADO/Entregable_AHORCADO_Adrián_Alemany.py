import os
import time
import psycopg  # Librería de PostgreSQL
from datetime import datetime
from psycopg.errors import OperationalError

def connect_to_db():
    """
    Intenta conectarse a la base de datos con reintentos.
    Esto es crucial porque la 'app' puede arrancar antes
    de que la 'db' esté 100% lista para aceptar conexiones.
    """
    # Obtenemos la URL de conexión del fichero .env
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("No se encontró DATABASE_URL en las variables de entorno")

    conn = None
    retries = 10
    print("Conectando a la base de datos...")
    while retries > 0:
        try:
            conn = psycopg.connect(db_url)
            print("¡Conexión exitosa a la base de datos!")
            return conn
        except OperationalError as e:
            print(f"Error: {e}")
            print(f"La base de datos no está lista. Reintentando en 5 segundos... ({retries} intentos restantes)")
            retries -= 1
            time.sleep(5)
    
    print("Error: No se pudo conectar a la base de datos después de varios intentos.")
    return None

def create_results_table(conn):
    """
    Crea la tabla de resultados si no existe,
    siguiendo la estructura que pediste.
    """
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS game_results (
                    id SERIAL PRIMARY KEY,
                    palabra VARCHAR(100) NOT NULL,
                    letras_acertadas TEXT,
                    letras_falladas TEXT,
                    intentos INTEGER NOT NULL,
                    tiempo TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            conn.commit()
            print("Tabla 'game_results' comprobada/creada con éxito.")
    except Exception as e:
        print(f"Error al crear la tabla: {e}")

def save_game_result(conn, palabra, acertadas, falladas, intentos):
    """
    Inserta una nueva fila en la tabla de resultados.
    """
    try:
        with conn.cursor() as cur:
            # Convertimos las listas de letras a texto
            letras_acertadas_str = ",".join(sorted(list(acertadas)))
            letras_falladas_str = ",".join(sorted(list(falladas)))

            cur.execute("""
                INSERT INTO game_results (palabra, letras_acertadas, letras_falladas, intentos, tiempo)
                VALUES (%s, %s, %s, %s, %s)
            """, (palabra, letras_acertadas_str, letras_falladas_str, intentos, datetime.now()))
            
            conn.commit()
            print(f"Resultado de la palabra '{palabra}' guardado en la BD.")
    except Exception as e:
        print(f"Error al guardar el resultado: {e}")

def play_game_mock():
    """
    Esta es una función de EJEMPLO.
    Aquí iría tu lógica real del juego del Ahorcado.
    Para este ejercicio, simplemente devolvemos un resultado fijo.
    """
    print("Jugando una partida de ejemplo...")
    time.sleep(2) # Simula el tiempo de juego
    
    palabra = "DOCKER"
    letras_acertadas = {'D', 'O', 'C', 'K', 'E', 'R'}
    letras_falladas = {'A', 'S', 'T'}
    intentos_totales = len(letras_acertadas) + len(letras_falladas)
    
    print(f"Partida de ejemplo terminada. Palabra: {palabra}")
    return palabra, letras_acertadas, letras_falladas, intentos_totales

# --- Flujo Principal de la Aplicación ---
if __name__ == "__main__":
    
    # 1. Conectar a la BD
    connection = connect_to_db()
    
    if connection:
        # 2. Asegurar que la tabla existe
        create_results_table(connection)
        
        # 3. Jugar la partida (aquí llamas a tu juego)
        palabra, acertadas, falladas, intentos = play_game_mock()
        
        # 4. Guardar el resultado en la BD
        save_game_result(connection, palabra, acertadas, falladas, intentos)
        
        # 5. Cerrar la conexión
        connection.close()
    else:
        print("No se pudo ejecutar la aplicación porque no hay conexión a la BD.")
