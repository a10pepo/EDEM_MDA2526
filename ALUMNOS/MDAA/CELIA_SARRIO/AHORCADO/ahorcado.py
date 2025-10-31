import os
import psycopg

url = os.getenv("DATABASE_URL")
connection = psycopg.connect(url)
cur = connection.cursor()
print("BD conectada con éxito")

def createIntentos ():
    query = """CREATE TABLE IF NOT EXISTS INTENTOS (
id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
palabra VARCHAR(100),
letras_acertadas VARCHAR(50),
letras_falladas VARCHAR(50),
intentos INTEGER,
tiempo TIMESTAMPTZ NOT NULL DEFAULT NOW()
);"""
    cur.execute(query)
    print("Tabla creada con éxito!")

createIntentos()
connection.commit()

letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Ñ"]

def Ahorcado():
    total = 0
    with open("palabras.txt", encoding="utf-8") as texto:
        for line in texto:
            palabra = line.strip().upper()
            intentos = 0
            letras_adivinadas = ''
            letras_falladas = ''
            for letra in letras:
                intentos += 1
                if letra in palabra:
                    letras_adivinadas += letra
                else:
                    letras_falladas += letra
                if all(l in letras_adivinadas for l in palabra):
                    total += intentos
                    break
                print(f"La palabra '{palabra}' se adivinó en {intentos} intentos.")
                query = """INSERT INTO INTENTOS (palabra, letras_acertadas,
                        letras_falladas, intentos) VALUES (%s, %s, %s, %s);"""
                cur.execute(query, (palabra, letras_adivinadas, letras_falladas, intentos))
                connection.commit()
    print(f"Total de intentos para todas las palabras: {total}") 
Ahorcado()
