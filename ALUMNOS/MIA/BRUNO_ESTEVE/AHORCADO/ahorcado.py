import string

# Inicializar la variable intento
intentos = 0

# Lista abecedario
abecedario_es = list(string.ascii_uppercase) 
indice_n = abecedario_es.index("N") 
abecedario_es.insert(indice_n + 1, "Ñ")
print(abecedario_es)


# Leer las palabras del fichero e imprimirlas
palabras = set()
with open("palabras.txt", encoding="utf-8") as doc_palabras:
    for line in doc_palabras:
        palabra = line.strip()
        n_letras = len(palabra)
        for letra in abecedario_es:
            intentos += 1
            n_aparicion = palabra.count(letra)
            n_letras = n_letras - n_aparicion
            if n_letras == 0:
                break

# Imprimimos el número de intentos
print(intentos)