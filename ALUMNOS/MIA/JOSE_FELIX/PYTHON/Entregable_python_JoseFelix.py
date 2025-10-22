# Ejercicio 1

# x = "Marina de Empresas 2025"
# print(len(x))
# print(x[0])

# # Ejercicio 2

# festivo=True
# if festivo:
#     print("Hoy es fiesta voy a echarme una siesta!!")
# else:
#     print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

# Ejercicio 3

# def ultimoCaracter(data):
#     if isinstance(data, str):
#         return data[-1]
#     else:
#         return "Debo ser ejecutada con un string"
# print(ultimoCaracter(88))

# Ejercicio 5 — Bad Words

def norm(s: str) -> str:
    return s.lower().strip()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra = input("Escribe algo ")
if not palabra or " " in palabra:
    print ("Introduce una sola palabra (sin espacios).")
    exit
else:
    actualizada= norm(palabra)

if actualizada in bad:
    print("NO CORRECTA.")
else:
    print("CORRECTA.")


