# Ejercicio 1 - Flor Sastre

# Se debe trabajar con una variable que contiene la información: “Marina de Empresas 2025”
variable: str = "Marina de Empresas 2025"  

# Muestra por consola la longitud de la variable
print (len(variable))

# Utilizando esa variable muestra por consola la primera letra.
print (variable[0])

#Define una variable festivo que sea de tipo booleano.
festivo: bool = True

#Crea una condición en la que sí festivo es verdadero se muestre por consola 
# “Hoy es fiesta voy a echarme una siesta!!” y sino que muestre por consola 
# “No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ”

if festivo:
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ")

    #Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter.

def ultimoCaracter(cadena: str):
    if type(cadena) == str:
        return cadena[-1]
    
#Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'

    else:
        return "Debo ser ejecutada con un string"


print(ultimoCaracter("Flor"))
print(ultimoCaracter(100))  

#Escribe un programa que pida una palabra por teclado y diga si está en la lista de palabras prohibidas 
# (bad_words.txt). La comparación debe ser insensible a mayúsculas .
#Material proporcionado (NO modificar)
#Se guarda el bloque que carga bad_words.txt en un set llamado bad (una palabra por línea):


#normalizacion y convierte minusculas, sin espacios
def norm(s: str) -> str:
    return s.lower().strip()

#cargo archivo
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

#pido palabra
palabra = input("Introduce una palabra: ")

#sihay espacios o vacia
if not palabra or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
    exit()

palabra_normalizada = norm(palabra)
if palabra_normalizada in bad:
    print("NO CORRECTA")
else:
    print("CORRECTA")
