##### EJERCICIO 1 #####

variable = "Marina de Empresas" #asignamos el nombre de la variable

print(len(variable)) #con print() mostramos por pantalla la longitud (len()) de la variable y el primer digito con [0]
print(variable[0])


##### EJERCICIO 2 #####

festivo = True #asignamos el valor booleano True a la variable festivo

if festivo == True: #hacemos un condicional, utilizamos el operador de asignacion (==) para decir que si festivo es True muestre una frase y si no muestre otra
    print("Hoy es fiesta voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de python :)")


##### EJERCICIO 3 (4) #####

#definimos la funcion ultimoCarcter a la cual se le introduce un valor (palabra)
def ultimoCaracter(palabra): 
    if type(palabra) != str: #con un condicional y el operador de asignacion != vemos si el tipo (type()) de la palabra no es una string(str) y se lo pedimos por pantalla
        return "Debo ser ejecutada con un string"
    else:
        return f"El ultimo caracter es: {palabra[-1]}" #si si que es una string mostramos directamente el ultimo caracter con [-1]

print(ultimoCaracter("hola")) #mostramos la funcion por pantalla para asegurarnos de que funciona


##### EJERCICIO 5 #####

#creamos esta funcion para normalizar las palabras del archivo txt
def norm(s:str):
    s = s.lower() #las pone todas en minusculas
    s = s.strip() #elimina espacios 
    return s

#ya dado, genera una lista que se rellena a partir de un archivo que nosotros creamos
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w)) #normaliza las palabras de la lista con la funcion creada por nosotros arriba

#pedimos por pantalla que se introduzca una palabra y la pasamos por nuestra funcion norm para asegurarnos de que esta en minusculas y sin espacios
palabra = str(input("Escriba una palabra: "))
palabra = norm(palabra)

#hacemos un condicional para verificar si la palabra escrita es solo una sin espacios o si no se introduce solo espacio blanco 
if not palabra.strip() or " " in palabra:
    print("Introduce una sola palabra (sin espacios)")
    
elif palabra in bad:  #si la palabra cumple con los criterios de arriba entonces se comprueba si esta en la lista bad con in
    print("NO CORRECTA")
else:
    print("CORRECTA")


