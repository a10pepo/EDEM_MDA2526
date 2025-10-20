#EJERCICIO 1
info: str="Marina de Empresas 2025"
print(f"La longitud de la cadena es: {len(info)}")
print(f"El primer carácter de la cadena es: {info[0]}")

#EJERCICIO 2
festivo: bool=True

if festivo:
    print("Hoy es fiesta voy a echarme una siesta")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

#EJERCICIO 4
def ultimoCaracter(palabra):
    if type(palabra)==str:
        return palabra[-1]
    else:
        return "Debo ser ejecutada con un string"

print(ultimoCaracter("Cocacola"))
print(ultimoCaracter(32))

#EJERCICIO 5
def norm(s: str) -> str:
    return s.lower().strip()


bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra=input("Dime una palabra: ")

if palabra == "" or " " in palabra:
    print("Introduce una sola palabra (sin espacios)")
elif norm(palabra) in bad:
    print(f"NO CORRECTA ({norm(palabra)} está en el .txt)")
else:
    print("CORRECTA")