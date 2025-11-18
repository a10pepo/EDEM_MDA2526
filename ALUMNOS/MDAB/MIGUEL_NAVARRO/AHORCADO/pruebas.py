import string

words = ["MURCIELAGO", "VIAJE", "EVADIR", "ZAPATO", "CIELO", "RECREO", "PIZARRA", "MATEMATICAS", "PROGRAMACION", "ORDENADOR"]
# letters = string.ascii_uppercase    # Guardo el abecedario
# letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"    # Abecedario manual
# letters = "AEIOUBCDFGHJKLMNPQRSTVWXYZ"
# letters = "EAOSRNIDLCTUMPBGVYQHFZJXKW"

total_strikes = 0                # Número de intentos totales en el ahorcado
for palabra in words:       # cada palabra
    letras_acertadas = ""   # string vacía
    letras_falladas = ""    # string vacía
    intentos = 0            # Número de intentos para esta palabra
    known_letters = 0
    for letra in letters:   # cada letra
        intentos += 1
        total_strikes +=1
        if letra in palabra:    # letra en la palabra?
            known_letters += palabra.count(letra)   # nº de letras adivinadas
            letras_acertadas += letra
        else:
            letras_falladas += letra
        if known_letters == len(palabra):
            break
    print(f"{intentos}")
print("Total =", total_strikes)
