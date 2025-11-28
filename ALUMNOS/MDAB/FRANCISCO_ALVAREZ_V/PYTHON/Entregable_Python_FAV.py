# Ejercicios entregables - Python Francisco Alvarez Varas

## Ejercicio 1
# 1. Se debe trabajar con una variable que contiene la información: “Marina de Empresas 2025” 

elSueño = "Marina de Empresas 2025"

# 2. Muestra por consola la longitud de la variable 

print(len(elSueño))

# 3. Utilizando esa variable muestra por consola la primera letra.

print(elSueño[0])

## Ejercicio 2
# 1. Define una variable festivo que sea de tipo booleano. 

festivo = True

# 2. Crea una condición en la que sí festivo es verdadero se muestre por consola.

if festivo:

# “Hoy es fiesta voy a echarme una siesta!!” y sino que muestre por consola 

    print("Hoy es fiesta voy a echarme una siesta!!")

# “No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ” 

else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ")


# ## Ejercicio 4

# 1. Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter. 

def ultimoCaracter(palabras):
    if type(palabras) is str:
        return palabras[-1]

# 2. Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'. 

    else:
        return 'Debo ser ejecutada con un string'
    
print(ultimoCaracter("Hola Sofi esperando el fin de semana para vernos en clase!, Saludos Fran"))
print(ultimoCaracter(246810))

# ## Ejercicio 5 — **Bad Words**

# Normalización

def norm(s: str) -> str:
    return s.strip().lower() 

# Carga de palabras malas

bad = set()              
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))


entra_input = input("Introduce una sola palabra: ")      
if not entra_input or ' ' in entra_input:                 
    print("Introduce una sola palabra (sin espacios).")
else:
    normal_input = norm(entra_input)  
    if normal_input in bad:
        print("NO CORRECTA")                  
    else:
        print("CORRECTA")                     