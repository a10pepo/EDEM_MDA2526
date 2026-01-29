import os, psycopg, time

def ahorcando_palabra(palabra, letras_acertadas, letras_falladas, intentos, tiempo):
    try:
        
        url = os.getenv("DATABASE_URL")
        connection = psycopg.connect(url)
        cur = connection.cursor()
        query = "INSERT INTO ahorcado (palabra, letras_acertadas, letras_fallads, intentos) VALUES (%s, %s, %s, %s)"
#         cur.execute("""INSERT INTO ahorcado (palabra, letras_acertadas, letras_fallads, intentos)
# VALUES ('GATO', 'A,G,O,T', 'B,C,D,E,F', 12);""")
        letras_acertadas="".join(sorted(letras_acertadas))
        letras_falladas="".join(sorted(letras_falladas))
        print(letras_falladas)
        cur.execute(query,(palabra, letras_acertadas, letras_falladas, intentos))
        connection.commit()
        print(cur.fetchall())

        print("Palabra ahorcada")
    except Exception as e:
        print("Imposiblre")



letras = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',  'V', 'W', 'X', 'Y', 'Z' ]

contador_total= 0

with open("palabras.txt", 'r', encoding="utf-8") as lista_palabras:
    for linea in lista_palabras:
        palabra = linea.strip().upper()
        letras_encontradas = set()
        letras_falladas = set()
        intentos = 0
        inicio = time.time()
        for letra in letras:
            intentos += 1
            if letra in palabra:
                letras_encontradas.add(letra)
                letras_acertadas = letras_encontradas.copy()
            else:
                letras_falladas.add(letra)
            if set(palabra) == letras_encontradas:
                tiempo = time.time() - inicio
                print(f"La palabra, {palabra}, fue encontrada en {intentos}")
                contador_total += intentos
                ahorcando_palabra(palabra, letras_acertadas, letras_falladas, intentos, tiempo)
                break
                
print(f"El numero total de intentos es de {contador_total} para las palabras proporcionadas")

