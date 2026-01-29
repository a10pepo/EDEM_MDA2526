# Ejercicio 1
texto = "Marina de Empresas 2025"

print(len(texto))
print(texto[0])


# Ejercicio 2
festivo = False

if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ")


# Ejercicio 4
def ultimoCaracter(s):
    if not isinstance(s, str):
        return 'Debo ser ejecutada con un string'
    return s[-1]


# Ejercicio 5
def norm(s: str) -> str:
    return s.strip().lower()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

entrada = input("Dame una sola palabra \n")

if entrada == "" or " " in entrada:
    print("Introduce una sola palabra (sin espacios)." )
else:
    palabra = norm(entrada)
    if palabra in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")