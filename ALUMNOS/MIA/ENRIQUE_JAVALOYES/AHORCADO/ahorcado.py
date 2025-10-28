
letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
letras_usadas =[]


palabras=[]
with open("palabras.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        palabras.append(linea.strip().upper())


intentos=0
for palabra in palabras:
    print(palabra)
    huecos = len(palabra)

    for letra in letras:
        intentos += 1
        if letra in palabra:

            repe = palabra.count(letra)
            huecos -= repe
            print(f'{letra} {repe} veces')

            if huecos == 0:
                break
            
print(intentos)


