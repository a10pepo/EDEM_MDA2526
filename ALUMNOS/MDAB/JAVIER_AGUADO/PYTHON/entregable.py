# EJERCICIO 1
nombre = "Marina de Empresas 2025"
print(len(nombre))
print(nombre[0])

# EJERCICIO 2
festivo: bool = True
if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!") 
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

# EJERCICIO 4
def ultimoCaracter(texto: str) -> str:
    if isinstance(texto, str):
        return texto[-1]
    else:
        return 'Debo ser ejecutada con un string'
    
# EJERCICIO 5
# Normalización
def norm(s: str) -> str:
    s = s.lower()
    s = s.lstrip()
    s = s.rstrip()
    return s

# Entrada
palabra = input("Dame una palabra: ")

# Validación
if palabra == "" or ' ' in palabra:
    print("Introduce una sola palabra (sin espacios).")
    exit()

# Comprobación
palabra = norm(palabra)

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

# Salida
if palabra in bad:
    print("NO CORRECTA")
else:
    
    print("CORRECTA")