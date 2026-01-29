#Lea las palabras de un fichero de texto, una por línea

palabras = []
letras = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

with open("palabras.txt", encoding="utf-8") as f:
    for linea in f:
        palabras.append(linea.strip())

intentos = 0

for palabra in palabras:
    aciertos = 0
    for letra in letras:
        intentos = intentos+1
        if letra in palabra:
            # print(letra,palabra)
            aciertos = aciertos + palabra.count(letra)
        if aciertos == len(palabra):
            break
print(f"Número total de intentos para adivinar todas las palabras: {intentos}")
print(f"Número total de aciertos:{aciertos}")


