import psycopg
import os
import time

palabras = []
letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]


def insert_intento(conexion, palabra, letras_acertadas, letras_falladas, intentos):
    try:
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO resultados_ahorcado (palabra, letras_acertadas, letras_falladas, intentos)
        VALUES (%s, %s, %s, %s); """, (palabra, letras_acertadas, letras_falladas, intentos))
        cursor.close()
        conexion.commit()
    except Exception as e:
        print("Error al insertar intento:", e)

def crear_tabla_palabras(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados_ahorcado(
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            palabra TEXT NOT NULL,
            letras_acertadas TEXT NOT NULL,
            letras_falladas TEXT,
            intentos INT,
            tiempo TIMESTAMP NOT NULL DEFAULT now()); """)
        cursor.close()
        conexion.commit()
    except Exception as e:
        print("Error al crear la tabla:", e)

def comprueba_resultados(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM resultados_ahorcado;")
        resultado = cursor.fetchone()
        print(f"Total de registros en la tabla resultados_ahorcado: {resultado[0]}")
        cursor.execute("SELECT * FROM resultados_ahorcado LIMIT 5;")
        resultado = cursor.fetchall()
        print("Primeros 5 registros:")
        for fila in resultado:
            print(fila)
        cursor.close()
        return resultado[0]
    except Exception as e:
        print("Error al comprobar resultados:", e)
        return 0

print("##################################################")
print("Iniciando Ahorcado con Base de Datos: SOLUCION C")
print("##################################################")

# Leer fichero desde variable

print("Cargando palabras desde palabras.txt")
# Leemos el fichero
with open("/app/palabras.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        palabra = linea.strip()
        if palabra:
            palabras.append(palabra)

if len(palabras) > 0:
    print("Palabras cargadas:", palabras)
else:
    print("No se han cargado palabras. Saliendo...")
    exit(1)

print("Conectando a la base de datos")
intentos_conexion = 0
conectado = False
while intentos_conexion < 5 and not conectado:
    try:
        # Conectamos a la base de datos
        conexion = psycopg.connect(os.getenv("DATABASE_URL"))
        if conexion:
            print("Conexión exitosa a la base de datos")
            conectado = True
        cursor = conexion.cursor()
    except Exception as e:
        print("Error al conectar a la base de datos, reintentando...")
        print(e)
        intentos_conexion += 1
        time.sleep(10)
        if intentos_conexion == 5:
            print("No se pudo conectar a la base de datos después de varios intentos.")
            exit(1)


print("Creando tabla de resultados si no existe")
crear_tabla_palabras(conexion)


# Empezamos a iterar sobre las palabras y letras
intentos = 0
for palabra in palabras:
    aciertos = 0
    letras_acertadas = ""
    letras_falladas = ""
    for letra in letras:
        intentos += 1
        if letra in palabra:
            aciertos += palabra.count(letra)
            letras_acertadas += letra
        else:
            letras_falladas += letra
        insert_intento(conexion, palabra, letras_acertadas, letras_falladas, intentos)
        if aciertos == len(palabra):
            break
    
print(f"Total de intentos para completar el juego: {intentos}")
comprueba_resultados(conexion)
conexion.close()    
