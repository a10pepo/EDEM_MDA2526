# # Ejercicios entregables 

# ## Ejercicio 1

#Creación de variable
texto = "Marina de Empresas 2025" 

#Longitud texto
print(len(texto))

#Muestra primera letra
print(texto[0])

# ## Ejercicio 2
# 1. Define una variable festivo que sea de tipo booleano. 

festivo = False

# 2. Crea una condición en la que sí festivo es verdadero se muestre por consola “Hoy es fiesta voy a echarme una siesta!!” y sino que muestre por consola “No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ” 

if festivo == True:
    print("Hoy es fiesta voy a echarme una siesta!!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")
    
# ## Ejercicio 4
# 1. Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter. 

def ultimoCaracter(texto): 
    if type (texto) != str:
        return (f"Debo ser ejecutada con un string")
    else:
        return (texto) [-1]
    

print(ultimoCaracter("Ayer me fui de viaje a Madrid"))

    
# ## Ejercicio 5 — **Bad Words**

#Normalización
def norm(s):
    return s.lower().strip()

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))
	
#Solicito palabra
entrada = input("Introduce una sola palabra: ")

#Validación
if not entrada or " " in entrada:
    print("Introduce una sola palabra (sin espacios).")
elif norm (entrada) in bad:
    print("NO CORRECTA")
else:
    print("CORRECTA")


    




