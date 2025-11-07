palabras = []
letras = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

with open("words.txt", "r", encoding="utf-8") as f:
    for line in f:
        palabras.append(line.strip())



intentos = 0

for palabra in palabras:
    aciertos = 0
    for letra in letras:
        intentos = intentos + 1
        if letra in palabra:
            print(letra, palabra)
            aciertos = aciertos + palabra.count(letra)
        if aciertos == len(palabra):
            break

print(intentos)
print(aciertos)
