import os
import sys
import psycopg
from datetime import datetime

url = os.getenv("DATABASE_URL")
connection = psycopg.connect(url)
cur = connection.cursor()
print("BD conectada con éxito")

def createTableAhorcado():
    try:
        query = """
        CREATE TABLE IF NOT EXISTS ahorcado_sinIA (
            id SERIAL PRIMARY KEY,
            palabra VARCHAR(255) NOT NULL,
            letras_acertadas VARCHAR(100),
            letras_fallidas VARCHAR(100),
            intentos INTEGER NOT NULL,
            tiempo TIMESTAMP NOT NULL
        );
        """
        cur.execute(query)
        connection.commit()
        print("Tabla ahorcado creada")
    except Exception as e:
        print("Error creando la tabla ahorcado", e)
# createTableAhorcado()

archivo = sys.argv[1]
with open(archivo, "r", encoding="utf-8") as f:
    lista = [linea.strip() for linea in f]
    print(lista)

abecedario = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

intentos_totales = 0

for palabra in lista:
    letras_acertadas = []
    intentos = 0
    letras_fallidas = []  
    
    for letra_a in abecedario:
        intentos += 1
        intentos_totales += 1
        
        for letra_l in palabra:
            if letra_a == letra_l and letra_a not in letras_acertadas:
                letras_acertadas.append(letra_a)
        
        if letra_a not in palabra and letra_a not in letras_fallidas:
            letras_fallidas.append(letra_a)
        
        letras_acertadas_str = "".join(sorted(letras_acertadas))
        letras_fallidas_str = "".join(sorted(letras_fallidas))
        cur.execute(
        "INSERT INTO ahorcado_sinIA (palabra, letras_acertadas, letras_fallidas, intentos, tiempo) VALUES (%s, %s, %s, %s, %s)",
        (palabra, letras_acertadas_str, letras_fallidas_str, intentos, datetime.now())
        )
        connection.commit()
        
        if len(letras_acertadas) == len(set(palabra)):
            print(f"Palabra: {palabra}; Intentos: {intentos}; Letras acertadas: {letras_acertadas}; Letras fallidas: {letras_fallidas}")
            break

print("Intentos totales:", intentos_totales)