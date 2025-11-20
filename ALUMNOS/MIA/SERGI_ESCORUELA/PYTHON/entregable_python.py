# # Ejercicios entregables - Python

# ## Ejercicio 1
# 1. Se debe trabajar con una variable que contiene la información: “Marina de Empresas 2025” 

nombre = "Marina de Empresas 2025"

# 2. Muestra por consola la longitud de la variable 
print(len(nombre))
# 3. Utilizando esa variable muestra por consola la primera letra.
print(nombre[0])

# ## Ejercicio 2
# 1. Define una variable festivo que sea de tipo booleano. 

festivo = True

# 2. Crea una condición en la que sí festivo es verdadero se muestre por consola “Hoy es fiesta voy a echarme una siesta!!” y sino que muestre por consola “No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ” 

if(festivo):
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")


# ## Ejercicio 4
# 1. Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter. 

def ultimoCaracter(ultimo):

    return print(ultimo[-1])

ultimoCaracter("Ultimo")


# 2. Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'. 

def ultimoCaracter(ultimo):
    if(isinstance(ultimo, str)):
        return print(ultimo[-1])
    else:
        return print("Debo ser ejecutada con un string")
    
    

ultimoCaracter("String Ultimo1")
ultimoCaracter(True)



# ## Ejercicio 5 — **Bad Words**

# ### Objetivo
# Escribe un programa que pida **una palabra** por teclado y diga si está en la lista de **palabras prohibidas** (`bad_words.txt`). La comparación debe ser **insensible a mayúsculas** .

# ##### Material proporcionado (NO modificar)
# Se guarda el bloque que **carga** `bad_words.txt` en un `set` llamado `bad` (una palabra por línea):

# ### Cargar bad_words.txt (una palabra por línea; # = comentario)
# ```
# bad = set()
# with open("bad_words.txt", encoding="utf-8") as f:
#     for line in f:
#         w = line.strip()
#         if w:
#             bad.add(norm(w))
# ```			

# ### Requisitos

# ### Normalización
# Crea la función `norm(s: str) -> str` que:
# - convierte a minúsculas,
# - quita espacios al inicio y al final.

# ### Entrada
# Pide al usuario **una sola palabra** con `input()`.

# ### Validación
# Si la entrada está vacía o contiene espacios, muestra exactamente:
# ```
# Introduce una sola palabra (sin espacios).
# ```
# y termina el programa.

# ### Comprobación
# - Normaliza la palabra introducida con `norm(...)`.
# - Comprueba si pertenece al conjunto `bad` cargado con el bloque proporcionado.

# ### Salida
# - Si pertenece: imprime **NO CORRECTA**
# - Si no pertenece: imprime **CORRECTA**

# ### Fichero de datos
# - `bad_words.txt` contiene **una palabra por línea**.

# ### ejemplo archivo bad_words.txt:
# ### una por línea 
# tonto
# idiota
# capullo


# ### Ejemplos para comprobar el ejercicio

# ##### Entrada: IDIOTA → Salida: NO CORRECTA (si idiota está en el .txt)

# ##### Entrada: saludo → Salida: CORRECTA

# ##### Entrada: hola mundo → Salida: Introduce una sola palabra (sin espacios).



def norm(s: str) -> str:
    s = s.lower().strip()
    return s



bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
     for line in f:
         w = line.strip()
         if w:
             bad.add(norm(w))

palabra = input("Una sola palabra: ")

palabra = norm(palabra)
if not palabra.strip() or " " in palabra:
    print("Introduce una sola palabra (sin espacios)")
else:
    correcta = True
    for palabraBad in bad:
        if(palabra==palabraBad):
            correcta = False

    if(correcta):
            print("CORRECTA")
    else:
            print("NO CORRECTA")