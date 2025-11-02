#Ejercicio 1
#1. Se debe trabajar con una variable que contiene la información: “Marina de Empresas 2025”
variable1="Marina de Empresas 2025"
#2. Muestre or consola la longitud de la variable. 
print(len(variable1))
#3. Utilizando esa variable muestra por consola la primera letra. 
print(variable1[0])

#Ejercicio 2. 
#1. Define una variable festivo que sea de tipo booleano. 
festivo=True
# festivo=False
#print(type(festivo))
#2.Crea una condición en la que sí festivo es verdadero se muestre por consola “Hoy es fiesta voy a echarme una siesta!!” y sino que muestre por consola “No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ”
if festivo==True:
    print ("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)") 

#Ejercicio 3
ultimoCaracter="Gemma"
print(type(ultimoCaracter))
#ultimocaracter=2
if isinstance(ultimoCaracter, str):
    print(ultimoCaracter[4])
else:
    print("debo ser ejecutada con un string")

#Ejercicio 4
def norm(s: str):
    return s.strip().lower()

#Cargamos las palabras prohibidas desde el archivo
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

#Entrada del usuario
# entrada="tonto"
# entrada="saludo"
entrada="Hola mundo"

#Validación
if not entrada or " " in entrada:
    print("Introduce una sola palabra (sin epacios)")
else: 
    palabra=norm(entrada)
    if palabra in bad:
        print ("No correcta")
    else: 
        print("correcta")