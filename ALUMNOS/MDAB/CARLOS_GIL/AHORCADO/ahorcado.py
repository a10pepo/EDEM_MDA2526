

palabras = []
letras = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
print(letras)


with open("palabras.txt", encoding="utf-8") as f:
    for line in f:
        # añade a la ray de palabras 
        palabras.append(line.strip())

print(palabras)

intentos=0
for palabra in palabras:
    aciertos=0
    for letra in letras:
        intentos=intentos+1
        if letra in palabra:
            print(letra,palabra)
            aciertos=aciertos+palabra.count(letra)

            # esto se utiliza para que deje de hacer intentos si ya se ha acertado en todos
        if aciertos == len(palabra): 
            break
print(intentos)
print(aciertos)

# with open("palabras.txt", encoding="utf-8") as docpalabras:
#     for line in docpalabras:
#         palabras = line.strip()
#         long = len(palabras)

#         for letra in letras :
#             print(f"esta es la palabra {letras}")
#             intentos += 1
#             apariciones = palabras.count(letra)

#             if letras == 0:
#                 break
#             print(intentos)
import os, psycopg

url = os.getenv("DATABASE_URL")
connection = psycopg.connect(url)
cur = connection.cursor()
print("BD conectada con éxito")
