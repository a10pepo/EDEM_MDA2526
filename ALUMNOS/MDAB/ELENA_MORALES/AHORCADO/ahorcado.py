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
