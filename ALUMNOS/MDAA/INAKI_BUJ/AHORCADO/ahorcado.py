import os, psycopg, requests 


url = os.getenv("DATABASE_URL")

connection = psycopg.connect(url)


##abrir conexion con la base de datos
cur = connection.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS tabla_ahorcado (
        palabra VARCHAR(100) NOT NULL,
        letras_acertadas VARCHAR(100) NOT NULL,
        letras_falladas VARCHAR(100) NOT NULL,
        intentos BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        tiempo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );"""
    
    
)

# cur.execute("""
# INSERT INTO tabla_ahorcado (palabra, letras_acertadas, letras_falladas, intentos, tiempo)
# VALUES (%s, %s, %s, %s, %s);""" (
# palabra,
# "".join(sorted(letras_acertadas)),
# "".join(sorted(letras_falladas)),
# intentos,
# datetime.now()
# ))
# conn.commit()

# # si ya tengo todas las letras de la palabra -> paro
# if set(palabra) <= letras_acertadas:
#     print(f"La palabra, {palabra} fue completada en {intentos} intentos.")
#     contador_total += intentos
#     break

# print(f"\nNúmero total de intentos para todas las palabras: {contador_total}")

# cur.close()
# conn.close()

# print("\nDatos guardados correctamente en la base de datos")

# ##con el cursor de la base de datos ejecutar la query del create table y
# ##debajo hacer un commit

letras = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
    'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]
    
intentos = 0


def norm(s: str) -> str:
    return s.upper().strip()


lista_palabras = set()
with open("palabras.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            lista_palabras.add(norm(w))

intentos = 0
for palabra in lista_palabras:
    aciertos = 0
    for letra in letras:
        intentos=intentos+1
        if letra in palabra:
            aciertos += palabra.count(letra)
            if aciertos == len(palabra):
                break
print (intentos)

    