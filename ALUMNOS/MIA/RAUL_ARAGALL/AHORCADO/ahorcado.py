letras = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',  'V', 'W', 'X', 'Y', 'Z' ]

contador_total= 0

with open("palabras.txt", 'r', encoding="utf-8") as lista_palabras:
    for linea in lista_palabras:
        palabra = linea.strip().upper()
        letras_encontradas = set()
        intentos = 0
        for letra in letras:
            intentos += 1
            if letra in palabra:
                letras_encontradas.add(letra)
            if set(palabra) == letras_encontradas:
                print(f"La palabra, {palabra}, fue encontrada en {intentos}")
                contador_total += intentos
                break
                
print(f"El numero total de intentos es de {contador_total} para las palabras proporcionadas")


