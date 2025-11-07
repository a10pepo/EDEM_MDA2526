## Librerias a usar
import sys
import os
import psycopg
import requests
import time
from collections import Counter
 
################# FUNCIONES A UTILIZAR
def createTableAhorcado():
    try:
        query = """
        DROP TABLE ahorcado;
        CREATE TABLE IF NOT EXISTS ahorcado(
            intentos INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            palabra VARCHAR(100),
            letras_acertadas VARCHAR(100),
            letras_falladas VARCHAR(100),
            tiempo TIMESTAMP
        )
        """
        cur.execute(query)
        connection.commit()
        print("Tabla creada")
    except Exception as e:
        print("Error creando tabla:", e)

def addIntento(palabra, letras_acertadas, letras_falladas):
    try:
        query = """
        INSERT INTO ahorcado(palabra, letras_acertadas, letras_falladas)
        VALUES(%s, %s, %s)
        """
        cur.execute(query, (palabra, letras_acertadas, letras_falladas))
        connection.commit()
        # print("Intento creado")

    except Exception as e:
        print("Error creando intento:", e)  

def getIntentos():
    try:
        query = """
        SELECT * 
        FROM ahorcado
        """
        cur.execute(query)
        rows = cur.fetchall()
        print("Intentos existentes:")
        for row in rows:
            print(row)
    except Exception as e:
        print("Error obteniendo intentos:", e)  


################################## CÓDIGO
#URL CONEXIÓN A BD
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")


# ## CONEXION A API RAE
url_api = "https://rae-api.com/api/random"

response = requests.get(url_api)
response.raise_for_status()
data = response.json()
palabra = data["data"]["word"] 

# print(palabra)

# Creamos la tabla AHORCADO
createTableAhorcado()

palabras = []
# Leer el archivo con palabras
with open(sys.argv[1], 'r') as archivo:
    lineas = archivo.readlines()
    # 'lineas' ahora es una lista de strings, cada uno es una línea
    for linea in lineas:
        palabras.append(linea.strip()) # .strip() elimina saltos de línea


# Unificamos todas las letras en una sola cadena (minúsculas)
todas = "".join(palabras).lower()

# Contamos frecuencia de cada letra
frecuencias = Counter(todas)

# Ordenamos por frecuencia (más - menos)
letras_ordenadas = [letra for letra, _ in frecuencias.most_common()]

# Añadimos las letras que no aparecen en ninguna palabra
abecedario_completo = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
    "l", "m", "n", "ñ", "o", "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y", "z"
]

# Completamos la lista con las faltantes
for letra in abecedario_completo:
    if letra not in letras_ordenadas:
        letras_ordenadas.append(letra)

# abecedario = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
abecedario = letras_ordenadas
intentos = 0
fallos_totales = 0
aciertos_totales = 0

# Recorremos la lista de palabras
for i in range(len(palabras)):
    palabra_actual = palabras[i].lower()
    len_palabra = len(palabra_actual) # Para no pasarnos
    aciertos = 0
    fallos = 0

    letras_acertadas_list = ""
    letras_falladas_list = ""

    # Recorremos el abecedario
    for i in range(len(abecedario)):
        letra_actual = abecedario[i]
        intentos += 1   
        # print (f"Letra actual: {letra_actual}, palabra actual: {palabra_actual}")
        # Si la letra está en la palabra
        if letra_actual in palabra_actual:
            n_letra = palabra_actual.count(letra_actual)
            # print(f"La letra {letra_actual} está un total de {n_letra} veces en la palabra {palabra_actual}")

            aciertos += n_letra
            letras_acertadas_list += letra_actual

            if aciertos == len_palabra:
                addIntento(palabra_actual, letras_acertadas_list, letras_falladas_list)
                letras_acertadas_list += letra_actual
                break

            # print(aciertos)

        else:
            fallos += 1
            letras_falladas_list += letra_actual
        
        addIntento(palabra_actual, letras_acertadas_list, letras_falladas_list)

    fallos_totales += fallos
    aciertos_totales += aciertos
    
print(f"Tarea completada con un total de {intentos} intentos.")
getIntentos()

