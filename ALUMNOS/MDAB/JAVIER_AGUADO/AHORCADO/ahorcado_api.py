import sys
import psycopg
import os
import requests
import time

def get_random_word():
    """Obtener una palabra aleatoria desde la API de la RAE"""
    try:
        url = "https://rae-api.com/api/random"
        headers = {"Accept": "application/json"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None
    
def main():
    # Conexión a la base de datos
    database_url = os.getenv("DATABASE_URL", "postgresql://usuario:password@localhost:5432/ahorcado_db")
    connection = psycopg.connect(database_url)
    cur = connection.cursor()
    
    contador_palabras = 0
    num_palabras = 6  # Número de palabras a solicitar
    intervalo = 10  # segundos entre cada solicitud

    print(f"Solicitando {num_palabras} palabras aleatorias de la RAE cada {intervalo} segundos:")
            

    print("Resultados del juego del ahorcado:")

    while contador_palabras < num_palabras:
        result = get_random_word() # Hace la llamada a la API

        if result and result.get("ok"): # Si obtiene respuesta
            contador_palabras += 1
            word_data = result["data"] # Obtiene la palabra del json
            palabra = word_data["word"].upper() # La pasa a mayúscula
            # Elimina acentos y diéresi
            palabra = palabra.replace('Á', 'A')
            palabra = palabra.replace('É', 'E')
            palabra = palabra.replace('Í', 'I')
            palabra = palabra.replace('Ó', 'O')
            palabra = palabra.replace('Ú', 'U')
            palabra = palabra.replace('Ü', 'U')
            palabra = palabra.replace('Ï', 'I')

            print(f"\nPalabra: {palabra}")

            # Simulación del "juego del ahorcado"
            letras_palabra = set(palabra) # Creamos un set de la palabra para saber cuántas letras únicas tiene (por si se repiten letras en la misma palabra)
            letras_acertadas = set() # Inicializamos un set donde guardaremos las letras que acertemos
            letras_falladas = set() # Inicializamos un set para las letras falladas
            intentos = 0  # Inicializamos los intentos para esta palabra
            # Fase 5: Optimización
            # for letra in "EAOSRNIDLCTUMPBGVYQHFJZXKW": # Recorremos todas las letras del abc según su frecuencias más alta en el español
            for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ": # Recorremos todas las letras del abc
                intentos += 1 # Añadimos un intento por cada letras que probamos
                if letra in letras_palabra: # Si esa letra está en nuestra palabra
                    letras_acertadas.add(letra) # La añadimos al set de letras acertadas
                else:
                    letras_falladas.add(letra) # Si no está, la añadimos a las falladas
                
                # Insertar en la base de datos
                cur.execute(
                    "INSERT INTO intento_ahorcado (palabra, letras_acertadas, letras_falladas, intentos) VALUES (%s, %s, %s, %s)",
                    (palabra, ''.join(sorted(letras_acertadas)), ''.join(sorted(letras_falladas)), intentos)
                )
                connection.commit()

                if letras_acertadas == letras_palabra: # Si ya hemos acertado todas la letras, es decir, nuestros set de letras de la palabra es igual que el set de letras acertadas
                    break # Terminamos el bucle de búsqueda de letras porque ya hemos acertado la palabra

            print(f"Palabra: {palabra} - Intentos: {intentos}")
        else:
            print("No se pudo obtener una palabra aleatoria.")

        time.sleep(intervalo) # Se espera 10 segundos antes de la siguiente llamada a la API

    
    # Consultar los últimos 100 intentos
    print("\n--- Top 100 intentos registrados ---")
    cur.execute("SELECT id, palabra, letras_acertadas, letras_falladas, intentos, tiempo FROM intento_ahorcado ORDER BY id ASC LIMIT 100")
    resultados = cur.fetchall()
    
    for row in resultados:
        print(f"Palabra: {row[1]} | Acertadas: {row[2]} | Falladas: {row[3]} | Intentos: {row[4]} | Tiempo: {row[5]}")
    
    # Cerrar conexión
    cur.close()
    connection.close()

if __name__ == "__main__":
    main()