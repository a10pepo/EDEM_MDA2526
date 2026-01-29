import os, psycopg, requests, unicodedata, time

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")



def norm(s: str) -> str:
    return s.upper().strip()


bad = set()
with open("palabras.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

contador = 0

# PROBABILIDAD DE ACIERTO MAS BAJA
# def recorrerPalabra(palabra):

#     alfabeto = [
#         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ',
#         'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
#     ]

#     aux = 0

#     letras_encontradas = set()
#     letras_falladas = set()

#     for a in alfabeto:
#         if a in palabra:
#             aux += 1
#             print("Letra encontrada")
#             letras_encontradas.add(a)
#         else:
#             aux += 1
#             print("Letra no encontrada")
#             letras_falladas.add(a)
#         if set(palabra) == letras_encontradas:
#             try:
#                 query = """INSERT INTO Ahorcado(palabra , letras_acertadas , letras_falladas , intentos)
#                 VALUES(%s , %s , %s , %s)
#                 """
#                 letras_encontradas2 = list(letras_encontradas)
#                 letras_falladas2 = list(letras_falladas)
#                 values = (palabra , letras_encontradas2 , letras_falladas2 , aux)
#                 cur.execute(query, values)
#             except Exception as e:
#                 print(e)

#             break

def eliminar_tildes(texto):
    # Normalizamos a forma NFD (descompone letras con acento)
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Reconstruimos la cadena sin marcas de acento, pero conservando ñ
    texto_sin_tildes = ''.join(
        c for c in texto_normalizado
        if unicodedata.category(c) != 'Mn' or c.lower() == 'ñ'
    )
    return texto_sin_tildes

# PROBABILIDAD DE ACIERTO MAS ALTA
def recorrerPalabra(palabra):

    alfabeto = ['E', 'A', 'O', 'S', 'R', 'N', 'I', 'D', 'L', 'C', 'T', 'U', 'M', 
        'P', 'B', 'G', 'V', 'Y', 'Q', 'H', 'F', 'Z', 'J', 'Ñ', 'X', 'K', 'W']

    aux = 0

    letras_encontradas = set()
    letras_falladas = set()

    for a in alfabeto:
        if a in palabra:
            aux += 1
            print("Letra encontrada")
            letras_encontradas.add(a)
        else:
            aux += 1
            print("Letra no encontrada")
            letras_falladas.add(a)
        if set(palabra) == letras_encontradas:
            try:
                query = """INSERT INTO Ahorcado(palabra , letras_acertadas , letras_falladas , intentos)
                VALUES(%s , %s , %s , %s)
                """
                letras_encontradas2 = list(letras_encontradas)
                letras_falladas2 = list(letras_falladas)
                values = (palabra , letras_encontradas2 , letras_falladas2 , aux)
                cur.execute(query, values)
            except Exception as e:
                print(e)

            break

        

    print(f"El numero de intentos ha sido {aux}")
    return aux


def obtenerUltimaPalabra():
    try:
        query = """SELECT *
        FROM Ahorcado
        ORDER BY id DESC
        LIMIT 1;"""
        cur.execute(query)
        print("Nuestras palabras: ",cur.fetchall(), flush = True)
    except Exception as e:
        print(e)

lista = list(bad)


# response = requests.get("https://rae-api.com/api/random")
# data = response.json()
# palabra = data["data"]["word"]


# palabra = palabra.upper()
# palabra = eliminar_tildes(palabra)
# print(palabra)
# recorrerPalabra(palabra)


# Bucle para pedir palabra cada 10 segundos
while True:
    try:
        response = requests.get("https://rae-api.com/api/random")
        data = response.json()
        palabra = data["data"]["word"]


        palabra = palabra.upper()
        palabra = eliminar_tildes(palabra)
        print(palabra, flush=True)
        recorrerPalabra(palabra)
        obtenerUltimaPalabra()
    except Exception as e:
        print("Error al solicitar la API:", e)

    connection.commit()
    
    
    # Esperamos 10 segundos antes de la siguiente petición
    time.sleep(10)


# for palabra in lista:
#     aux = []
#     if palabra in aux:
#         continue
#     else: 
#         contador += recorrerPalabra(palabra)
#         aux.append(palabra)
#     print(aux)

def createTableAhorcado():
    try:
        query = """CREATE TABLE Ahorcado (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            palabra VARCHAR(50) NOT NULL,
            letras_acertadas VARCHAR(50) NOT NULL,
            letras_falladas VARCHAR(100) NOT NULL,
            intentos INTEGER NOT NULL,
            tiempo TIMESTAMPTZ DEFAULT NOW()
        );"""
        cur.execute(query)
        print("Tabla creada AAAAAAAAAAAAAAAAAAAAAA")
    except:
        print('La tabla ya existe XXXXXXXXXXXXXXXXXXXXXX')

def getAhorcado():
    query = "SELECT * FROM Ahorcado;"
    cur.execute(query)
    print("Nuestros empleados:",cur.fetchall())



getAhorcado()

connection.commit()

print(contador)



