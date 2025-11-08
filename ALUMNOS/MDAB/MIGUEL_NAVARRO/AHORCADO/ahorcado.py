import string, sys, os, psycopg

# URL CONEXIÓN A BD
url = os.getenv("DATABASE_URL")
# CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")

# Leo el fichero y lo guardo
with open(sys.argv[1], 'r') as f:
    content = f.read()
    words = content.split()
letters = string.ascii_uppercase    # Guardo el abecedario

# Número de intentos en el ahorcado
total_strikes = 0
for word in words:          # cada palabra
    known_letters = 0
    for letter in letters:  # cada letra
        total_strikes += 1
        if letter in word:  # letra en la palabra ?
            known_letters += word.count(letter) # letras adivinadas
        if known_letters == len(word):
            break
    
print("Total strikes: ", total_strikes)



cur.execute("""CREATE TABLE IF NOT EXISTS ahorcado(
            id                  INTEGER GENERATED ALWAYS AS INDENTITY PRIMARY KEY,
            palabra             VARCHAR(30) NOT NULL,
            letras_acertadas    VARCHAR(30),
            letras_falladas     VARCHAR(30),
            intentos            INTEGER,
            tiempo              TIMESTAMPZ DEFAULT NOW()
            );""")







# Adivinar primera palabra




