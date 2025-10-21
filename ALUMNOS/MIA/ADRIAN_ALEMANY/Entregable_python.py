#1.1
texto = "Marina de Empresas 2025"

#1.2
print("Longitud del texto:", len(texto))

#1.3
print("Primera letra:", texto[0])


#2.1
festivo = False  # cambia a True para probar la otra opción

#2.2
if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")


#4.1 y 4.2
def ultimoCaracter(cadena):
    if type(cadena) != str:
        return "Debo ser ejecutada con un string"
    

    if len(cadena) > 0:
        return cadena[len(cadena) - 1]
    else:
        return ""


#5.1
# Función para normalizar la palabra (minúsculas y sin espacios)
def norm(s):
    return s.lower().strip()


# Cargar el archivo de palabras prohibidas (bad_words.txt)
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:  # si no está vacía la línea
            bad.add(norm(w))


# Pedir palabra al usuario
palabra = input("Introduce una palabra: ")

# Validar si está vacía o tiene espacios
if palabra.strip() == "" or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra_norm = norm(palabra)  # normalizamos la palabra
    if palabra_norm in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")
