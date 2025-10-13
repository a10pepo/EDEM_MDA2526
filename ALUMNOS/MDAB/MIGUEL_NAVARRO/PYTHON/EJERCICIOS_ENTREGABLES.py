"""
EJERCICIOS ENTREGABLES - PYTHON
(1)
"""

"""
print("Ejercicio 1")
var1 = "Marina de Empresas 2025"
print(f"La variable '{var1}' tiene {len(var1)} caracteres.")
print(f"La primera letra es la {var1[0]}")

print("\nEjercicio 2")
festivo = False
if festivo == True:
    print("Hoy es fiesta, voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

print("\nEjercicio 3")
def ultimoCaracter(cadena: str):
    if not isinstance(cadena, str):
        print("Debo ser ejecutada con un string")
    else:
        print(f"'{cadena[-1]}' es el último carácter")
ultimoCaracter("Python")
"""
"""
print("\nEjercicio 4")

ad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra = input("Introduzca una palabra: ")
print(f"La palabra es {palabra}")
"""


badword = ["word1", "word2", "word3", "word4"]
word_wanted = "word3"
for word in badword:
    print(f"Checking word: {word}")
    if word == word_wanted:
        print(f"Word found! {word} is on the list")
        break
    print(f"The word '{word}' is not on the list")
print("Ended program")

numeros = [1, 2, 3, 4, 5, 6, 7]
for num in numeros:
    if num % 2 == 0:
        print(f"Saltando el número par: {num}")
        continue
    print(f"Procesando número impar: {num} (su cuadrado es {num * num})")
print("Fin del programa tras el bucle")