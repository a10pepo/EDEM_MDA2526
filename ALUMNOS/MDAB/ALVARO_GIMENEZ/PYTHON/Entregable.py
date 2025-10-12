#Ejercicio 1

var1="Marina de Empresas 2025"
print(len(var1))
print(var1[0])

#Ejercicio 2

festivo=True
if festivo == True: 
    print("Hoy es fiesta voy a echarme una siesta!!") 
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")

#Ejercicio 4

def ultimocaracter(texto): 
    if type(texto) != str: 
       print("Debo ser ejecutada con un string")
    else: 
        print(texto[len(texto)-1])

ultimocaracter("hola")

#Ejercicio 5 - Bad words

#Creamos funcion de normalizacion
def norm(s):
    normalizado=s.strip()
    normalizado=normalizado.lower()
    return normalizado

#Guardamos las bad words en un set 
bad = set()
with open(r"C:\Users\alvar\Documents\GitHub\EDEM_MDA2526\ALUMNOS\MDAB\ALVARO_GIMENEZ\PYTHON\bad_words.txt", mode="r", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

entrada=input("Introduce una palabra")

a=0

if entrada=="" or entrada!=entrada.replace(' ', ''): 
    print("Introduce una sola entrada sin espacios")
else:
    entrada_normalizada=norm(entrada)
    for words in bad: 
         if words==entrada_normalizada: 
            print("NO CORRECTA")
            a=1
            break
if a != 1: 
      print("CORRECTA")