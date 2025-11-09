import os, psycopg, requests, time, unicodedata
from datetime import datetime
abecedario = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
with open('palabras.txt', 'r', encoding='utf-8') as archivo:
    palabras = [linea.strip() for linea in archivo]


def quitar_acentos_conservando_n(texto):
    originales = "áéíóúÁÉÍÓÚüÜ"
    reemplazos = "aeiouAEIOUuU"
    tabla = str.maketrans(originales, reemplazos)
    return texto.translate(tabla)

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
        letras_adiv = []
        letras_falladas = []
        letra_abecedario = 0
        letras_adivinadas = 0
    print(f'Los intentos son {intentos}')
    return lista_dict


tiempo_inicio = time.perf_counter()    
lista_dict = ahorcado(palabras, abecedario)
tiempo_fin = time.perf_counter()
duracion_segundos = tiempo_fin - tiempo_inicio
print(f"\nLa función 'ahorcado()' tardó: {duracion_segundos:.6f} segundos en completarse.")                


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

cur.execute("DROP TABLE IF EXISTS palabras")
connection.commit()

def crearTabla():
    try:
        query = """CREATE TABLE IF NOT EXISTS palabras (
        palabra VARCHAR,
        letras_acertadas VARCHAR,
        letras_falladas VARCHAR,
        intentos INTEGER,
        tiempo TEXT)"""
        cur.execute(query)
        connection.commit()
        print("Tabla creada")
    except Exception as e:
        print("Error creando tabla:", e)

crearTabla()
def createPalabra(palabra, letras_acertadas, letras_falladas, intentos, tiempo):
    try:
        query = "INSERT INTO palabras (palabra, letras_acertadas, letras_falladas, intentos, tiempo) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (palabra, letras_acertadas, letras_falladas, intentos, tiempo))
        connection.commit()
        print("Registro creado")
    except Exception as e:
        print("Error creando registro:", e)
for i in lista_dict:
    createPalabra(i['palabra'], i['letras_acertadas'], i['letras_falladas'], i['intentos'], i['tiempo'])

cur.execute("SELECT * FROM palabras;")
print(cur.fetchall())
connection.commit()


while True:
    arr = []    
    request = requests.get("https://rae-api.com/api/random")
    word=request.json().get('data')['word'].upper()
    print(word)
    arr.append(quitar_acentos_conservando_n(word))
    lista = ahorcado(arr, abecedario)
    time.sleep(10)

## ME CREO UNA FUNCION NUEVA EN LA QUE VOY A TRATAR DE OPTIMIZAR

abecedario = 'AEIOUBCDFGHJKLMNÑPQRSTVWXYZ'

def ahorcado2(palabras, abecedario):
    lista_dict = []
    intentos = 0
    for palabra in palabras:
        letras_adiv = []
        letras_falladas = []
        letra_abecedario = 0
        letras_adivinadas = 0
        while letras_adivinadas < len(palabra):
            if abecedario[letra_abecedario] in palabra:
                letras_adivinadas += palabra.count(abecedario[letra_abecedario])
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
    print(f'Los intentos son {intentos}')
    return lista_dict


tiempo_inicio = time.perf_counter()    
lista_dict = ahorcado2(palabras, abecedario)
tiempo_fin = time.perf_counter()
duracion_segundos = tiempo_fin - tiempo_inicio
print(f"\nLa función 'ahorcado()' tardó: {duracion_segundos:.6f} segundos en completarse.")  