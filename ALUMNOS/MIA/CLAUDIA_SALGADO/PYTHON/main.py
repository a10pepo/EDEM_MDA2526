
##### ENTREGABLE PYTHON - Clàudia Salgado

### EJERCICIO 1
variable = "Marina de Empresas 2025"

# Muestra por consola la longitud de la variable
print(len(variable))

#Muestra por consola la primera letra de la variable
print(variable[0])


### EJERCICIO 2
festivo:bool = True

# Muestra un mensaje u otro dependiendo de si es festivo o no
if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")


### EJERCICIO 4
# Recibe una string y devuelve su último carácter
def ultimoCaracter(texto:str):
    if type(texto)==str:
        return texto[-1]
    else: # Si no es string muestra el siguiente mensaje:
        return "Debo ser ejecutada con un string"
    
print(ultimoCaracter("Hola"))


# EJERCICIO 5

# Quita los espacios iniciales/finales y pone la string en minúsculas
def norm(s: str):
    s=s.strip()
    s=s.lower()
    return s
    
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

# Pide al usuario una palabra y la normaliza
entrada = input("Escribe una palabra: ")
palabra = norm(entrada)

# Si la palabra normalizada está vacía o tiene espacios intermedios avisa al usuario, si no, comprueba si está en la lista y la aprueba o no.
if palabra == "" or " " in palabra:
    print("Introduce una sola palabra (sin espacios): ")
elif palabra in bad:
    print("NO CORRECTA")
else:
    print("CORRECTA")