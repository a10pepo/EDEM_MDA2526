import os   
import requests
import psycopg


url = os.getenv("DATABASE_URL")
connection = psycopg.connect(url)
cur = connection.cursor()
print("Conexión exitosa a la base de datos.")


def conectar_api():
    url_api = f"https://rae-api.com/api/words/random"
    try:
        response = requests.get(url_api)
        data = response.json()
        print(data)
        return data
    except requests.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None

def crear_tabla():
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ahorcado_api (
                id SERIAL PRIMARY KEY,
                palabra VARCHAR(100) NOT NULL,
                letras_acertadas VARCHAR(100),
                letras_falladas VARCHAR(100),
                intentos_restantes INT NOT NULL,
            );
        """)
        connection.commit()
        print("Tabla ahorcado_api creada exitosamente.")
    except Exception as e:
        print(f"Error al crear la tabla: {e}")

crear_tabla()


def insertar_datos(palabra, letras_acertadas, letras_falladas, intentos_restantes):
    try:
        cur.execute("""
            INSERT INTO ahorcado_api (palabra, letras_acertadas, letras_falladas, intentos_restantes)
            VALUES (%s, %s, %s, %s)
        """, (palabra, letras_acertadas, letras_falladas, intentos_restantes))
        connection.commit()
        print(f"Datos insertados para la palabra: {palabra}")
    except Exception as e:
        print(f"Error al insertar datos: {e}")

palabras = []
intentos = 0
for palabra in palabras:
    letras_acertadas = ""
    letras_falladas = ""
    aciertos = 0

    for letra in palabra:
        intentos += 1
        if letra in palabra:
            letras_acertadas += letra
            aciertos += 1
        else:
            letras_falladas += letra
        insertar_datos(palabra, letras_acertadas, letras_falladas, intentos)
        if aciertos == len(palabra):
            break

print("Todos los datos han sido insertados con éxito.")
cur.close()
connection.close()
