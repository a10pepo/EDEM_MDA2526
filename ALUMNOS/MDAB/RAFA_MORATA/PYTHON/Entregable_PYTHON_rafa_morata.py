# EJERCICIO 1
lugar = "Marina de Empresas 2025"


print("Longitud de la variable:", len(lugar))


print("Primera letra:", lugar[0])



# EJERCICIO 2
festivo = False 


if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")



# EJERCICIO 4
def ultimoCaracter(texto):
    if type(texto) != str:
        return "Debo ser ejecutada con un string"
    else:
        return texto[-1]


print(ultimoCaracter("Esto es PYHTON"))
print(ultimoCaracter(1234)) 


# EJERCICIO 5
def norm(s: str) -> str:
    return s.lower().strip()


bad = set()

with open("bad_words.txt") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))


palabra = input("Introduce una palabra: ")


if palabra.strip() == "" or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra_normal = norm(palabra)

    if palabra_normal in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")
