# # Ejercicios entregables - Python

# ## Ejercicio 1
# 1. Se debe trabajar con una variable que contiene la información: “Marina de Empresas 2025” 

# 2. Muestra por consola la longitud de la variable 

# 3. Utilizando esa variable muestra por consola la primera letra.

# //---------------------SOLUCION--------------------//

# nombre = "Marina de Empresas 2025"
# print(len(nombre))
# print(nombre[0])

# //---------------------SOLUCION--------------------//

# ## Ejercicio 2
# 1. Define una variable festivo que sea de tipo booleano. 

# 2. Crea una condición en la que sí festivo es verdadero se muestre por consola “Hoy es fiesta voy a echarme una siesta!!” y sino que muestre por consola “No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ” 

# //---------------------SOLUCION--------------------//

# festivo = False
# if festivo == True:
#     print("Hoy es fiesta voy a echarme una siesta!!")
# else:
#     print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ")

# //---------------------SOLUCION--------------------//

# ## Ejercicio 4
# 1. Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter. 

# 2. Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'. 

# //---------------------SOLUCION--------------------//

# def fun_ultimoCaracter(cadena):
#     try:
#         float(cadena)
#         return "Debo ser ejecutada con un string" 
#     except:
#         return cadena[-1]

# //---------------------SOLUCION--------------------//

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

# //---------------------SOLUCION--------------------//

# bad = set()
# with open("bad_words.txt", encoding="utf-8") as f:
#     for line in f:
#         w = line.strip()
#         if w:
#             bad.add(norm(w))

# def fun_norm(s):

#     s = s.lower()

#     for letra in s:
#         if(letra == " "):
#             s = s[1:]                                   #Se queda con toda la cadena excepto el primer carácter
#         else: break

#     cadena_invertida = s[::-1]                          #Invierte la cadena. Hola pasaría a ser aloH

#     for letra in cadena_invertida:
#         if(letra == " "):
#             cadena_invertida = cadena_invertida[1:]
#         else: break

#     s = cadena_invertida[::-1]                          #Desinvierte la cadena

#     return s


palabra_introducida = input("Por favor, introduce una sola palabra: ")

if palabra_introducida == "":
    print("Introduce una sola palabra (sin espacios).")
    
else:
   for letra in palabra_introducida:
      if letra == " ":
        print("Introduce una sola palabra (sin espacios).")
        break
