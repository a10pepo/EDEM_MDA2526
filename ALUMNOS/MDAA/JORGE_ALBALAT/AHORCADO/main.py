import os, psycopg
from datetime import datetime
abecedario = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
with open('palabras.txt', 'r', encoding='utf-8') as archivo:
    palabras = [linea.strip() for linea in archivo]

def ahorcado(palabras, abecedario):
    lista_dict = []
    intentos = 0
    letras_adivinadas = 0
    letra_abecedario = 0
    letras_adiv = []
    letras_falladas = []
    for palabra in palabras:
        while letras_adivinadas < len(palabra):
            if abecedario[letra_abecedario] in palabra:
                letras_adivinadas += palabra.count(abecedario[letra_abecedario])
                #print(f'La letra {abecedario[letra_abecedario]} esta en la palabra')
                intentos += 1
                letras_adiv.append(abecedario[letra_abecedario])
                letra_abecedario += 1
                dict = {'palabra':palabra, 'letras_acertadas':letras_adiv, 'letras_falladas':letras_falladas,
                        'intentos':intentos, 'tiempo':datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                lista_dict.append(dict)
            else:
                intentos += 1
                letras_falladas.append(abecedario[letra_abecedario])
                letra_abecedario += 1
                dict = {'palabra':palabra, 'letras_acertadas':letras_adiv, 'letras_falladas':letras_falladas,
                        'intentos':intentos, 'tiempo':datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                lista_dict.append(dict)
        letra_abecedario = 0
        letras_adivinadas = 0
    print(f'Los intentos son {intentos}')
    return lista_dict
    
                
lista_dict = ahorcado(palabras, abecedario)

try:
    #URL CONEXIÓN A BD 
    url = os.getenv("DATABASE_URL")
    #CONEXIÓN A BD
    connection = psycopg.connect(url)
    # Cursor
    cur = connection.cursor()
    print("BD conectada con éxito")
except:
    print("Error conectando a la BD")

def crearTabla():
    try:
        query = """CREATE TABLE IF NOT EXISTS palabras (
        id INTEGER PRIMARY KEY,
        palabra VARCHAR,
        letras_acertadas VARCHAR,
        letras_falladas VARCHAR,
        intentos INTEGER,
        tiempo TIMESTAMPZ)"""
        cur.execute(query)
        connection.commit()
        print("Tabla creada")
    except Exception as e:
        print("Error creando tabla:", e)

crearTabla()
def createPalabra(palabra, letras_acertadas, letras_falladas, intentos, tiempo):
    try:
        query = "INSERT INTO palabas (palabra, letras_acertadas, letras_falladas, intentos, tiempo) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (palabra, letras_acertadas, letras_falladas, intentos, tiempo))
        connection.commit()
        print("Registro creado")
    except Exception as e:
        print("Error creando registro:", e)
for i in lista_dict:
    createPalabra(i['palabra'], i['letras_acertadas'], i['letras_falladas'], i['intentos'], i['tiempo'])

cur.execute("SELECT species, COUNT(*) FROM palabras;")
