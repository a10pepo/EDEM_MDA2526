# # Ejercicio 1
# # 1.	Se debe trabajar con una variable que contiene la información: “Marina de Empresas 2025”
# # 2.	Muestra por consola la longitud de la variable
# # 3.	Utilizando esa variable muestra por consola la primera letra.
mensaje = "Marina de Empresas 2025"
print("Longitud:", len(mensaje))
print("Primera letra:", mensaje[0])

# # Ejercicio 2
# # 1.	Define una variable festivo que sea de tipo booleano.
# # 2.	Crea una condición en la que sí festivo es verdadero se muestre por consola “Hoy es fiesta voy a echarme una siesta!!” y sino que muestre por consola “No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ”
festivo = True  
if festivo:	
        print("Hoy es fiesta voy a echarme una siesta!!")
else:
	    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

# # Ejercicio 4
# # 1.	Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter.
# # 2.	Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'.

def ultimoCaracter(texto):
    if type(texto) != str:
        return 'Debo ser ejecutada con un string'
    return texto[-1]

print(ultimoCaracter("Hola"))   
print(ultimoCaracter(42))      

# # EJERCICIO 5
# Escribe un programa que pida una palabra por teclado y diga si está en la lista de palabras prohibidas (bad_words.txt). 
# La comparación debe ser insensible a mayúsculas

def norm(s: str):
       return s.lower().strip()  #para que de mayusculas y quite espacios

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra= input("introduce palabra:")

if palabra == '' or ' ' in palabra:
      print(f"introduce una palabra solo(sin espacios)")
else:
    if norm(palabra) in bad:
            print("no correcto")
    else:
            print("correcto")

            


       
