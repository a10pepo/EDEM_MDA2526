# Ejercicio 1

mde = "Marina de Empresas 2025"

print(len(mde))

print(mde[0])

# Ejercicio 2

festivo = False

if festivo == True:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

# Ejercicio 4 (el 3 no se encuentra en el archivo EJERCICIOS_ENTREGABLES.md)

def ultimoCaracter(x):
    if type(x)==str:
        print(x[-1])
    else: 
        print("Debo ser ejecutada con un string")

# Ejercicio 5

def norm(s : str) -> str:
    return s.lower().strip()

entrada = input("Introduce una palabra: ")

if not entrada or " " in entrada:
    print("Introduce una sola palabra (sin espacios).")
    exit()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

if entrada in bad:
    print("NO CORRECTA")
else:
    print("CORRECTA")