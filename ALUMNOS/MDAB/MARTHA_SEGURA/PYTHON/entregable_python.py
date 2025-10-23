#EJERCICIO 1
#1. Se debe trabajar con una variable que contiene la información: "Marina de Empresas 2025"
texto = "Marina de Empresas 2025"
#2. Longitud de la variable
print(len(texto))
#3. mostrar por consola la primera letra
print (texto[0])

#EJERCICIO 2
#1. Define una variable festivo que sea de tipo booleano
festivo = True
#2. Crea una condición en la que sí festivo es verdadero se muestre por consila "Hoy es fiesta voy a echarme una siesta!!" y sino que muestre por consola "no es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)"
if festivo:
    print ("Hoy es fiesta voy a echarme una siesta!!")
else:
    print ("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

#EJERCICIO 3(4)
#1. Crea la función ultimoCaracter debe recibir un tipo string debe devolver el string "Debo ser ejecutada con un string"
def ultimoCaracter (texto):
    if type (texto) == str:
        return texto[-1]  
    else:
        return "Debo ser ejecutada con una string"
print(ultimoCaracter(8))

#EJERCICIO 4 (5)
#insensible a Mayus
def norm (palabra):
    return palabra.lower().strip()
#cargar bad_words.txt (copiado de ejercicio)
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))
#pedir una palabra
pedir_palabra=input("Por favor, intruduce una palabra:")
if pedir_palabra.strip() == "" or " " in pedir_palabra:
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra_norm = norm(pedir_palabra)
#correcta o no correcta
    if palabra_norm in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")    