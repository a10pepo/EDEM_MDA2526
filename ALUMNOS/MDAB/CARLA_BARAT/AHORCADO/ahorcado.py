palabras = []
letras = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
print(letras)


with open("palabras.txt", encoding= "utf-8") as f:
    for line in f:
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
        if aciertos == len(palabra):
            break
print(intentos)
print(aciertos)

# #como lo haría pedro
# import sys
# palabras =[]

# letras = ["A","B","C","D"]

# with open (palabras.txt, "r") as f:
#     for linea in f:
#         palabras.append(linea.strip())

# intentos = 0
# for palabra in palabras:
#     for letra in letras:
#         intentos=intentos+1
#         if letra in palabra:
#             print(letra,palabra)
#             aciertos= aciertos + 1
#         if aciertos == len(palabra):
#             break

# print(intentos)
# print(aciertos)


import os, psycopg

url = os.getenv("DATABASE_URL")
connection = psycopg.connect(url)
cur = connection.cursor()
print("BD conectada con éxito")
