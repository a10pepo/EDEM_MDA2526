########################## AHORCADO ########################################
import sys
#FICHERO PALABRAS 
#LEER FICHERO ARRAY PALABRAS
#ARRAY LETRAS
#ITERAR ARRAY PALABRAS con print palabra

def norm(s: str):
    return s.strip().lower()

#Cargamos las palabras prohibidas desde el archivo
palabra = set()
import os

# Construye la ruta correcta (misma carpeta del script)
ruta = os.path.join(os.path.dirname(__file__), "palabras.txt")

with open("palabra.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            palabra.add(w.lower().strip())

abecedario = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's',
    't', 'u', 'v', 'w', 'x', 'y', 'z'
]



intentos = 0

for x in palabra:
    x_str = str(x)
    aciertos = 0  
    letras_acertadas = ""
    letras_falladas = ""
    
    for i in abecedario:
        intentos += 1

        if i in x:
            aciertos += x.count(i)
            letras_acertadas += i
        else:
            letras_falladas +=i
      
        if aciertos == len(x):
            break  
        

print(intentos)



