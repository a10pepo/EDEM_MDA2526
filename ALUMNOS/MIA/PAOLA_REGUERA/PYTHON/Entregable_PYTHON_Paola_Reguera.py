# Ejercicio 1
texto= "Marina de Empresas 2025"

print(len(texto))
print(texto[0])

# Ejercicio 2
festivo= True
if festivo== True:
    print ("Hoy es fiesta voy a echarme una siesta!!")
else:
    print ("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

# Ejercicio 3
def ultimoCaracter(cadena):
    if type(cadena) != str:
        return 'Debo ser ejecutada con un string'
    else:
        return cadena[-1]

print(ultimoCaracter("test")) 

#Ejercicio 5
def norm(s: str) -> str:
    return s.lower().strip()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra= input("Introduce una palabra:")

if not palabra or " " in palabra:
    print("Introduce una sola palabra (sin espacios)")
    raise SystemExit

palabra_normalizada= norm(palabra)
if palabra_normalizada in bad:
    print ("NO CORRECTA")
else:
    print("CORRECTA")