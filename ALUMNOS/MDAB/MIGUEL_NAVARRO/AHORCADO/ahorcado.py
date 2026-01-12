import string, sys, os, psycopg, time, requests, json

# URL CONEXIÓN A BD
url = os.getenv("DATABASE_URL")
# CONEXIÓN A BD
while True:
    try:
        connection = psycopg.connect(url)
        print("BD conectada con éxito")
        break
    except psycopg.OperationalError:
        print("La base de datos se está conectando... espere 2 segundos")
        time.sleep(2) # Le doy 2 segundos por si  tarda en cargar
# Cursor
cur = connection.cursor()

# Leo el fichero y lo guardo
with open(sys.argv[1], 'r') as f:
    content = f.read()
    words = content.split()
# letters = string.ascii_uppercase          # Alfabeto (string.ascii)
# letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"    # Alfabeto (manual)
letters = "EAOSRNIDLCTUMPBGVYQHFZJXKW"      # Ordenador por frecuencia general español


# CREO LA TABLA (si no existe)
cur.execute("""CREATE TABLE IF NOT EXISTS ahorcado(
            id                  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            palabra             VARCHAR(30) NOT NULL,
            letras_acertadas    VARCHAR(30),
            letras_falladas     VARCHAR(30),
            intentos            INTEGER,
            tiempo              TIMESTAMPTZ DEFAULT NOW(),
            UNIQUE (palabra, intentos)
            );""")
connection.commit()

def insertAhorcado():   # insertar filas (intentos de ahorcado letra por letra) en la tabla
    try:
        query = """
        INSERT INTO ahorcado
        (palabra, letras_acertadas, letras_falladas, intentos)
        VALUES (%s, %s, %s, %s)"""
        cur.execute(query, (palabra, letras_acertadas, letras_falladas, intentos))
    except: # Exception as e:
        "nothing" # print("Error inserting try:", e)

# ADIVINO LAS PALABRAS DE palabras.txt Y GUARDO LOS INTENTOS EN LA TABLA ahorcado
intentos_totales = 0                # Número de intentos totales en el ahorcado
for palabra in words:       # cada palabra
    letras_acertadas = ""   # string vacía
    letras_falladas = ""    # string vacía
    intentos = 0            # Número de intentos para esta palabra
    known_letters = 0
    for letra in letters:   # cada letra
        intentos += 1
        intentos_totales +=1
        if letra in palabra:    # letra en la palabra?
            known_letters += palabra.count(letra)   # nº de letras adivinadas
            letras_acertadas += letra
        else:
            letras_falladas += letra
        insertAhorcado()
        if known_letters == len(palabra):
            break
    print(f"{palabra} - {intentos} intentos")
connection.commit()
print("Intentos totales: ", intentos_totales)

# ACCEDO a la API
try:
    url = "https://rae-api.com/api/random"
    headers = {"Accept": "application/json"}
except requests.exceptions.RequestException as e:
    print("Error accessing to url", e)

# OBTENGO PALABRA de la API de la RAE cada 10 segundos
while True:
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        palabra = data["data"]["word"].upper()
    except requests.exceptions.RequestException as e:
        print("Error getting new word:", e)
    
    # RESUELVO LA PALABRA
    intentos = 0            # Número de intentos para esta palabra
    letras_acertadas = ""   # string vacía
    letras_falladas = ""    # string vacía
    known_letters = 0
    for letra in letters:   # cada letra
        intentos += 1
        if letra in palabra:    # letra en la palabra?
            known_letters += palabra.count(letra)   # nº de letras adivinadas
            letras_acertadas += letra
        else:
            letras_falladas += letra
        insertAhorcado()    # la introduzco en la base de datos
        if known_letters == len(palabra):
            break
    print(f"{palabra} - {intentos} intentos")
    time.sleep(10)  # Espera 10 segundos y vuelve a empezar con otra palabra

connection.commit() # Guardo los intentos en la base de datos

# Cierro la conexión
cur.close()
connection.close()
