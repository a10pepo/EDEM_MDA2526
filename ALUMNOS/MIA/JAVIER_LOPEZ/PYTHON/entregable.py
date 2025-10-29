#Ejercicio1
frase= "Marina de Empresas 2025"
print(len(frase))
print(frase[0])


#Ejercicio2
festivo=True
if festivo==True:
    print("Hoy es fiesta voy a echarme una siesta")

else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")


#Ejercicio4
def ultimoCaracter(texto):
    if type(texto)!= str:
        print("Debo ser ejecutada con un string")

    else: 
        uc=texto[-1]
        return uc

#Ejercicio5
def norm(texto):
    t=texto.strip().lower()
    return t

bad = set()
with open("badwords.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

t=input("Dime una palabra: ")
t_norm=norm(t)
if " " in t_norm or t_norm=="":
    print("Introduce una sola palabra (sin espacios)")
elif t_norm in bad:
    print("NO CORRECTA")
else: 
    print("CORRECTA")
