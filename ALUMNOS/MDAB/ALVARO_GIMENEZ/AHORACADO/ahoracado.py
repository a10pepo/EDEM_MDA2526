# Tomamos las palabras del fichero de texto
lista_palabras = []
with open("palabras.txt", mode="r", encoding="utf-8") as file:
    for line in file:
        lista_palabras.append(line.rstrip('\n'))

print(lista_palabras)

# Generamos el diccionario de letras e inicializamos contador de intentos
diccionario_letras = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","ñ","o","p","q","r","s","t","u","v","w","x","y","z"]
contador_intentos = 0 

# Iteramos sobre todas las palabras
for palabra in lista_palabras: 
    
    palabra_sin_duplicados = set(palabra.lower())  # letras únicas en minúscula
    letras_encontradas = []
    contador_local=0

    # Simulamos probar letra por letra del alfabeto
    for letra in diccionario_letras:
        contador_local+=1
        contador_intentos += 1  # Cada prueba cuenta como intento, para todas las palabras
        if letra in palabra_sin_duplicados:
            letras_encontradas.append(letra)
        
        # Ya hemos encontrado las letras, salimos del bucle
        if len(letras_encontradas) == len(palabra_sin_duplicados):
            print(contador_local)
            break

print(contador_intentos)
