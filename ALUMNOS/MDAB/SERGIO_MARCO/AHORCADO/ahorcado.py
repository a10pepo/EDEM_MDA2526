
import os, sys, psycopg, datetime

#URL CONEXIÓN A BD. Definida en la variable de entorno DATABASE_URL del .env

url = os.getenv("DATABASE_URL")

#CONEXIÓN A BD con intentos y tiempo de espera

for i in range(10):
    try:
        connection = psycopg.connect(url)
        print("BD conectada con éxito")
        break
    except psycopg.OperationalError as e:
        print(f"Intento {i+1}: la BD aún no está lista. Esperando...")
        time.sleep(2)
else:
    print("No se pudo conectar a la BD tras varios intentos.")
    exit(1)

# Cursor.
# Crea un cursor, que es un objeto que permite ejecutar comandos SQL.
# - El cursor es como un "canal" entre tu código y la base de datos: puedes enviar consultas (SELECT, INSERT, etc.) y recibir resultados.
cur = connection.cursor()
print("Cursor creado con éxito")

#=============================================#
#=========== CREACIÓN TABLA ==================#
#=============================================#

cur.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY,
                palabra TEXT,
                letras_acertadas TEXT,
                letras_falladas TEXT,
                intentos INT,
                tiempo TIMESTAMPTZ
            );
        """)

connection.commit()

#--------------------------
archivo = sys.argv[1]  # toma el primer argumento después del nombre del script

#Lee el archivo .txt
with open(archivo, 'r', encoding='utf-8') as f:
    palabras = [palabra.strip() for palabra in f]

abecedario = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g',
    'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'ñ', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z'
]

contador_intentos = 0
lista_registros = []    # lista de tuplas de registros
for palabra in palabras:

    palabra_minusculas = palabra.lower()
    letras_unicas = len(set(palabra_minusculas))
    contador_letras_acertadas = 0
    letras_acertadas = ""
    letras_falladas = ""


    for letra in abecedario:
        
        if contador_letras_acertadas == letras_unicas:
            break

        else:

            if letra in palabra_minusculas:
                letras_acertadas = letra + letras_acertadas
                contador_letras_acertadas += 1
                contador_intentos += 1
                continue           

            else:
                letras_falladas = letra + letras_falladas
                contador_intentos += 1
                continue
            
        ahora = datetime.now()
        ahora_str = ahora.strftime("%Y-%m-%d %H:%M:%S")
        lista_registros.append((palabra,letras_acertadas,letras_falladas,))

