import numpy as np
import os 
import psycopg



#URL CONEXIÓN A BD 
print("Leyendo variable de entorno DATABASE_URL...")
url = os.getenv("DATABASE_URL")

#CONEXIÓN A BD
print(url)
print("Conectando a la BD...")

connection = psycopg.connect(url)
# Cursor
try:
    cur = connection.cursor()
    print("BD conectada con éxito")
except Exception as e:
    print("Error conectando a la BD")

#SQL
def creartabla():
    query = '''TRUNCATE TABLE ahorcadologs;'''
    cur.execute(query) 
    connection.commit()
    query = '''CREATE TABLE IF NOT EXISTS ahorcadologs (palabra TEXT,
      letras_acertadas VARCHAR(30),
      letras_falladas VARCHAR(30),
      intentos INTEGER NOT NULL,
      tiempo TIMESTAMPTZ NOT NULL DEFAULT NOW());'''
    cur.execute(query) 
    connection.commit()

def logIntento():
    try:
        query = """INSERT INTO ahorcadologs (palabra, letras_acertadas, letras_falladas, intentos) 
        VALUES (%s, %s, %s, %s);"""
        cur.execute(query)
        print("log añadido")
    except:
        print('Error creando log de intento')
    
def printtable():
    query = "SELECT * FROM ahorcadologs;"
    cur.execute(query)
    print(cur.fetchall())


# Obtener palabras desde archivo

with open("palabras.txt", "r", encoding="utf-8") as archivo:
    palabras10 = [linea.strip() for linea in archivo]
print(palabras10)

# Letras ordenadas según la frecuencia de uso en español: De 216 a 157 intentos.
alfabeto = ['e', 'a', 'o', 's', 'r', 'n', 'i', 'd', 'l', 'c', 't', 'u', 'm', 'p', 'b', 'g', 'v', 'y', 'q', 'h', 'f', 'z', 'j', 'ñ', 'x', 'k', 'w']
palabras = np.array(palabras10)
letras = np.array(alfabeto)

creartabla()

def ahorcado():
    intentos = 0
    for palabra in palabras:
        
        aciertos = 0
        intentos_palabra = 0
        acertadas = ''
        falladas = ''
        for letra in letras:
            intentos += 1
            intentos_palabra += 1
            if letra in palabra:
                acertadas += letra
                aciertos += palabra.count(letra)
                try:
                    query = """INSERT INTO ahorcadologs (palabra, letras_acertadas, letras_falladas, intentos) 
                        VALUES (%s, %s, %s, %s);"""
                    cur.execute(query, (palabra, acertadas, falladas, intentos_palabra))
                    connection.commit()
                    #print(f"log añadido para {palabra}")
                except:
                        print('Error creando log de intento')
                if aciertos == len(palabra):                    
                    print(f'Palabra "{palabra}" adivinada en {intentos_palabra} intentos.')
                    break
            else:
                falladas += letra
                try:
                    query = """INSERT INTO ahorcadologs (palabra, letras_acertadas, letras_falladas, intentos) 
                        VALUES (%s, %s, %s, %s);"""
                    cur.execute(query, (palabra, acertadas, falladas, intentos_palabra))
                    connection.commit()
                    #print(f"log añadido para {palabra}")
                except:
                        print('Error creando log de intento')
                continue
    print(f'Todas las palabras adivinadas en {intentos} intentos.')
    #print(query = '''SELECT * FROM ahorcadologs;''')
    print("Contenido de la tabla ahorcadologs: ")
    printtable()



ahorcado()