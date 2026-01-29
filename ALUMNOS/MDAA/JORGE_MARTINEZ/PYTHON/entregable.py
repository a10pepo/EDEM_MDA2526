#EJERCICIO 1

# Definimos la variable
texto = "Marina de Empresas 2025"

# Mostramos la longitud de la variable
longitud = len(texto)
print("La longitud de la variable es:", longitud)

# Mostramos la primera letra
primera_letra = texto[0]
print("La primera letra es:", primera_letra)

#EJERCICIO 2

# Definimos la variable booleana
festivo = False

# Condicional
if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

#EJERCICIO 4 (3)

def ultimoCaracter(texto):
    # Comprobamos si el parámetro es un string
    if type(texto) != str:
        return "Debo ser ejecutada con un string"
    # Devolvemos el último carácter del texto
    return texto[-1]

# Para ver un ejemplo uso estos prints:
print(ultimoCaracter("Marina de Empresas 2025"))  # Ultimo caracter tiene que devolver → '5'
print(ultimoCaracter(12345)) # al no ser un string tiene que devolver: 'Debo ser ejecutada con un string'

#EJERCICIO 5 - BAD WORDS

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

