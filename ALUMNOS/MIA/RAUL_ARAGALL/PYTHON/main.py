
# -------- EJERCICIO 1 --------

# nombre = "Marina de Empresas 2025"

# print(len(nombre))
# print((nombre)[0])


# -------- EJERCICIO 2 --------

# festivo = True

# if festivo:
#     print("Hoy es fiesta voy a echarme una siesta!!")
# else:
#     print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ")

# -------- EJERCICIO 4 --------

# def ultimo_caracter(palabra):
#     return ultimo_caracter[-1]

# palabra = "Marina de Empresas"

# if palabra:
#     print(ultimo_caracter(palabra))
# else:
#     print("Debo ser ejecutada con un string")

# -------- EJERCICIO 5 --------

def norm(s: str) -> str:
    return s.strip().lower()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra = input("Introduce una palabra: ") 

if palabra == "" or " " in palabra:
    print("No has introducido ninguna palabra.")

elif norm(palabra) in bad:
    print(f"La palabra, ({norm(palabra)}) es una palabra malsonante.")
else:
    print("La palabra introducida es correcta.")    