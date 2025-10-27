# texto = "Marina de empresas 2025"
# print (texto)
# print (len(texto))
# print (texto[0])

# festivo = True

# if festivo:
#     print("Hoy es fiesta voy a echarme una siesta!!")
# else:
#     print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python")

# print(festivo)

# def ultimocaracter(texto):
#     if type(texto) == str:
#         return texto [-1]
#     else:
#         return "Debo ser ejecutada con un string"

# print (ultimocaracter("David"))
# print (ultimocaracter(2025))


def norm(s):
    s=s.lower()
    s=s.strip()
    return s

bad_words=set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w=line.strip()
        if w:
            bad_words.add(norm(w))

bad_word=input("Da un insulto: ")
bad_word=norm(bad_word)
if " " in bad_word:
    print("Introduce una sola palabra (sin espacios).")
elif bad_word in bad_words:
    print("¡NO ES CORRECTA!")
else:
    print("¡ES CORRECTA!")

