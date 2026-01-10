import os
import psycopg
import time

url = os.getenv("DATABASE_URL")

connection = psycopg.connect(url)
cur = connection.cursor()
print("BD conectada con éxito")


abecedario = ['E', 'A', 'O', 'S', 'R', 'N', 'I', 'D', 'L', 'C', 'T', 'U', 'M', 'P', 'B', 'G', 'V', 'Y', 'Q', 'H', 'F', 'Z', 'J', 'Ñ', 'X', 'K', 'W']

intentos_totales = 0


with open("./fichero.txt", 'r', encoding='utf-8') as archivo:
    palabras = [linea.strip().upper() for linea in archivo.readlines()]


def insertPalabra(palabra, letras_acertadas, letras_falladas, intentos):
    try:
        query = """
            INSERT INTO palabras (palabra, letras_acertadas, letras_falladas, intentos)
            VALUES (%s, %s, %s, %s);
        """
        values = (palabra, 
                  ', '.join(letras_acertadas), 
                  ', '.join(letras_falladas), 
                  intentos)
        cur.execute(query, values)
        connection.commit()
        print(f"'{palabra}' insertada correctamente.")
    except Exception as e:
        print("Error insertando palabra:", e)
        connection.rollback()

for palabra in palabras:
    palabra_original = palabra
    letras_acertadas = []
    letras_falladas = []
    intentos = 0

    for letra in abecedario:
        intentos += 1
        intentos_totales += 1
        if letra in palabra:
            letras_acertadas.append(letra)
            palabra = palabra.replace(letra, "")
            if len(palabra) == 0:
                break
        else:
            letras_falladas.append(letra)

    insertPalabra(palabra_original, letras_acertadas, letras_falladas, intentos)

print("Proceso completado.")
print("INTENTOS TOTALES:", intentos_totales)

cur.close()
connection.close()
