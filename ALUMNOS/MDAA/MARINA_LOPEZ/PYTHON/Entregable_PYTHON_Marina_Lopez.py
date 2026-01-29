# Ejercicio 1

texto = "Marina de Empresas 2025"
print(len(texto))
print(texto[0])


# Ejercicio 2
festivo=True
if festivo == True:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python")

# Ejercicio 4

def ultimoCaracter(frase):
    if type(frase) == str:
        return frase[-1]
    else: 
        return "Debe ser ejecutada con un string"
print(ultimoCaracter("Marina de Empresas 2025"))
print(ultimoCaracter(2025))

# Ejercicio 5

#Normalización

def norm(s: str) -> str:
    return s.strip().lower()


bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

#Entrada
palabra= input("Dime una palabra:")

#validacion
if not palabra or " " in palabra:
    print("Introduce una sola palabra (sin espacios)")
    raise SystemExit

#Comprobación
palabra_normalizada = norm(palabra)

#salida
if palabra_normalizada in bad:
    print("La palabra no es correcta")
else:
    print(f"{palabra} es correcta")