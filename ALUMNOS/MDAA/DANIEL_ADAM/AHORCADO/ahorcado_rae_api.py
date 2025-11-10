import numpy as np
import os 
import psycopg
import requests



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


# Obtener letras
alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
letras = np.array(alfabeto)


# Obtener palabras desde API (caída): ConnectTimeout: HTTPSConnectionPool(host='api.rae.es', port=443): Max retries exceeded with url: /api/random 

try:
    url_rae = "https://rae-api.com/api/random"
    response_rae = requests.get(url_rae)
    palabra_rae = response_rae.json()['data']['word'].lower()

except:
    print("Error al conectar con la API de la RAE")
    exit

print(f'Palabra obtenida de la RAE: {palabra_rae}')

print('Creando tabla ahorcadologs')
creartabla()
print('Tabla ahorcadologs creada')

def ahorcado():
    intentos = 0
           
    aciertos = 0
    intentos_palabra = 0
    acertadas = ''
    falladas = ''
    for letra in letras:
        intentos += 1
        intentos_palabra += 1
        if letra in palabra_rae:
            acertadas += letra
            aciertos += palabra_rae.count(letra)
            try:
                query = """INSERT INTO ahorcadologs (palabra, letras_acertadas, letras_falladas, intentos) 
                        VALUES (%s, %s, %s, %s);"""
                cur.execute(query, (palabra_rae, acertadas, falladas, intentos_palabra))
                connection.commit()
                print(f"log añadido para {palabra_rae}")
            except:
                    print('Error creando log de intento 1')
            if aciertos == len(palabra_rae):                    
                print(f'Palabra "{palabra_rae}" adivinada en {intentos_palabra} intentos.')
                break
            else:
                falladas += letra
                try:
                    query = """INSERT INTO ahorcadologs (palabra, letras_acertadas, letras_falladas, intentos) 
                        VALUES (%s, %s, %s, %s);"""
                    cur.execute(query, (palabra_rae, acertadas, falladas, intentos_palabra))
                    connection.commit()
                    #print(f"log añadido para {palabra}")
                except:
                        print('Error creando log de intento 2')
                continue
    print(f'Todas las palabras adivinadas en {intentos} intentos.')
    #print(query = '''SELECT * FROM ahorcadologs;''')
    print("Contenido de la tabla ahorcadologs: ")
    printtable()



ahorcado()