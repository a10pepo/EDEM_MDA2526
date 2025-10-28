#EJERCICIO 1
#Se debe trabajar con una variable que contiene la información: “Marina de Empresas 2025”
variable = "Marina de Empresas 2025"

# Muestra por consola la longitud de la variable
print(f"La longitud es {len(variable)}")

# Utilizando esa variable muestra por consola la primera letra.
print(f"La primera letra es: {variable[0]}")



#EJERCICIO 2
# Define una variable festivo que sea de tipo booleano.
festivo = False

# Crea una condición en la que sí festivo es verdadero se muestre por consola “Hoy es fiesta voy a echarme una siesta!!” y sino que muestre por consola “No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ”
if festivo:
    print("Hoy es fiesta voy a echarme una siesta!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")


#EJERCICIO 4 (y el 3???)
#Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter.
def ultimoCaracter(s):
    if type(s) != str:
        return 'Debo ser ejecutada con un string'
    
    if len(s) == 0:
        return 'El string está vacío'
        
    return s[-1]

print(ultimoCaracter("Hola caracola")) # Funciona
print(ultimoCaracter(123))           # Devuelve el error
print(ultimoCaracter(True))          # Devuelve el error


#EJERCICIO 5 - Bad words
def norm(s: str) -> str:
    return s.lower().strip()
#Convierte a minúsculas y quita espacios al inicio/final.
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra_usuario = input("Introduce una palabra: ")
if not palabra_usuario or ' ' in palabra_usuario:
    print("Introduce una sola palabra (sin espacios).")
else:
    palabra_norm = norm(palabra_usuario)
    if palabra_norm in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")