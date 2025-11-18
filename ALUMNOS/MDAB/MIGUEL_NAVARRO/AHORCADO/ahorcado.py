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
        time.sleep(2)
# Cursor
cur = connection.cursor()

# Leo el fichero y lo guardo
with open(sys.argv[1], 'r') as f:
    content = f.read()
    words = content.split()
# letters = string.ascii_uppercase          # Alfabeto (string.ascii)
# letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"    # Alfabeto (manual)
letters = "EAOSRNIDLCTUMPBGVYQHFZJXKW"      # Ordenador por frecuencia general español

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

def insertAhorcado():   # insertar filas (intentos realizados) en la tabla
    try:
        query = """
        INSERT INTO ahorcado
        (palabra, letras_acertadas, letras_falladas, intentos)
        VALUES (%s, %s, %s, %s)"""
        cur.execute(query, (palabra, letras_acertadas, letras_falladas, intentos))
    except: # Exception as e:
        "nothing" # print("Error inserting try:", e)

"""
total_strikes = 0                # Número de intentos totales en el ahorcado
for palabra in words:       # cada palabra
    letras_acertadas = ""   # string vacía
    letras_falladas = ""    # string vacía
    intentos = 0            # Número de intentos para esta palabra
    known_letters = 0
    for letra in letters:   # cada letra
        intentos += 1
        total_strikes +=1
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
print("Intentos totales: ", total_strikes)
"""

try:
    url = "https://rae-api.com/api/random"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
except requests.exceptions.RequestException as e:
    print("Error accessing to url:", e)

print(data["data"]["word"], "es la palabra")
palabra = "cara"
print(palabra, "tiene", {len(palabra)}, "letras")

intentos = 0            # Número de intentos para esta palabra
letras_acertadas = ""   # string vacía
letras_falladas = ""    # string vacía
known_letters = 0

for letra in letters:   # cada letra
    intentos += 1
    if letra in palabra:    # letra en la palabra?
        known_letters += palabra.count(letra)   # nº de letras adivinadas
        letras_acertadas += letra
        print(letra, letras_acertadas)
    else:
        letras_falladas += letra
    # insertAhorcado()
    if known_letters == len(palabra):
        break
print(f"{palabra} - {intentos} intentos")
connection.commit()

# cur.close()
# connection.close()
