letters = "EAOSRNIDLCTUMPBGVYQHFZJXKW"      # Ordenador por frecuencia general españo

word = "cara"
palabra = word.upper()
print(palabra, "tiene", len(palabra), "letras")

intentos = 0            # Número de intentos para esta palabra
letras_acertadas = ""   # string vacía
letras_falladas = ""    # string vacía
known_letters = 0

for letra in letters:   # cada letra
    intentos += 1
    if letra in palabra:    # letra en la palabra?
        known_letters += palabra.count(letra)   # nº de letras adivinadas
        letras_acertadas += letra
        print(letra, known_letters)
    else:
        letras_falladas += letra
    # insertAhorcado()
    if known_letters == len(palabra):
        break
print(f"{palabra} - {intentos} intentos")
