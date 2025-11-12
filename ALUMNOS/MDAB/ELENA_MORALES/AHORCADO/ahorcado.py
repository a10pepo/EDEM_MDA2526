# Fase 1: Codificación

numero_intentos = 0

#Esto lo hacemos para traernos el archivo, si cambiamos una palabra en palabras.txt, se cambia automáticamente, y no hace falta cambiarlo a mano
listapalabras = []
with open ("palabras.txt", mode="r", encoding="utf-8") as file:
    for line in file:
        listapalabras.append(line.rstrip("\n"))
print(listapalabras)

letras = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

for palabra in listapalabras:
    print(palabra)
    aciertos = 0
    for letra in letras:
        numero_intentos += 1
        if letra in palabra:
            aciertos = aciertos + palabra.count(letra)
            print(letra, palabra)
        if aciertos == len(palabra):
            break

print(numero_intentos)


# Conexión y creación de la tabla

import os, psycopg
url = os.getenv("DATABASE_URL")
connection = psycopg.connect(url)
cur = connection.cursor()
print("BD conectada con éxito")


cur.execute("""
    CREATE TABLE IF NOT EXISTS ahorcado (
    id SERIAL PRIMARY KEY,
    palabra VARCHAR(100) NOT NULL,
    letras_acertadas INT NOT NULL,
    letras_falladas INT NOT NULL,
    intentos INT NOT NULL,
    tiempo TIMESTAMP
);
    """ )
connection.commit()
print("Tabla creada con éxito")

# Insertar datos en la tabla

for palabra in listapalabras:
    aciertos = 0
    fallos = 0
    numero_intentos = 0
    for letra in letras:
        numero_intentos += 1
        if letra in palabra:
            aciertos = aciertos + palabra.count(letra)
        else:
            fallos = fallos + 1
        if aciertos == len(palabra):
            break

    cur.execute("""
        INSERT INTO ahorcado (palabra, letras_acertadas, letras_falladas, intentos, tiempo)
        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
    """, (palabra, aciertos, fallos, numero_intentos))
    connection.commit()
    print(f"Datos insertados para la palabra: {palabra}")
print("Todos los datos han sido insertados con éxito")
cur.close()
connection.close()
print("Conexión cerrada")

# Consulta de datos
import os, psycopg
url = os.getenv("DATABASE_URL")         
connection = psycopg.connect(url)
cur = connection.cursor()
print("BD conectada con éxito")

cur.execute("SELECT * FROM ahorcado;")
rows = cur.fetchall()
for row in rows:
    print(row)
cur.close()
connection.close()
print("Conexión cerrada")



