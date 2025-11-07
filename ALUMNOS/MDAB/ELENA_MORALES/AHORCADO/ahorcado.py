# Fase 1: Codificación

from atexit import register


numero_intentos = 0

#Esto lo hacemos para traernos el archivo, si cambiamos una palabra en palabras.txt, se cambia automáticamente, y no hace falta cambiarlo a mano
listapalabras = []
with open ("palabras.txt", mode="r", encoding="utf-8") as file:
    for line in file:
        listapalabras.append(line.rstrip("\n"))
print(listapalabras)

letras = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

for palabra in listapalabras:
    print(palabra)
    aciertos = 0
    for letra in letras:
        numero_intentos += 1
        if letra in palabra:
            aciertos = aciertos + palabra.count(letra)
            print(letra, palabra)
        if aciertos == len(palabra):
            break

print(numero_intentos)


# FASE 3: Conexión y creación de la tabla

from psycopg import sql
from datetime import datetime
import os   
import psycopg
def conectar_bd():
    conexion = psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return conexion

def crear_tabla():
    return """
    CREATE TABLE IF NOT EXISTS ahorcado (
    id SERIAL PRIMARY KEY,
    palabra VARCHAR(100) NOT NULL,
    letras_acertadas INT NOT NULL,
    letras_falladas INT NOT NULL,
    intentos INT NOT NULL,
    tiempo TIMESTAMP
);
    """
register(crear_tabla)


# FASE 3.1: Inserción de resultados en la base de datos

def insertar_resultado(palabra, letras_acertadas, letras_falladas, intentos):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    consulta = sql.SQL("""
        INSERT INTO ahorcado (palabra, letras_acertadas, letras_falladas, intentos, tiempo)
        VALUES (%s, %s, %s, %s, %s)
    """)
    tiempo_actual = datetime.now()
    cursor.execute(consulta, (palabra, letras_acertadas, letras_falladas, intentos, tiempo_actual))
    conexion.commit()
    cursor.close()
    conexion.close()
    print("Resultado insertado correctamente en la base de datos.")

