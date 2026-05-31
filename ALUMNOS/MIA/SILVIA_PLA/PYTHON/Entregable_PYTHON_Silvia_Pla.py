#Ejercicio1
texto= ("Marina de Empresas 2025")
print(len(texto))
print(texto[0])


#Ejercicio2
festivo=True
if festivo==True:
    print("“Hoy es fiesta voy a echarme una siesta!!")
else:
    print ("“No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ”")

#Ejercicio4
def ultimoCaracter(cadena):
    if type(cadena) == str:         # comprobamos si es una cadena
        return cadena[-1]           # devolvemos el último carácter
    else:
        return "Debo ser ejecutada con un string"
print(ultimoCaracter("Marina de Empresas 2025"))  # devuelve "5"
print(ultimoCaracter(123))                        # devuelve "Debo ser ejecutada con un string"

#Ejercicio5

#Crea la función norm(s: str) -> str que:
# convierte a minúsculas,
# quita espacios al inicio y al final.
def norm(s: str) -> str:
    return s.lower().strip()
#Material proporcionado (NO modificar):
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))
#Entrada. 
# Pide al usuario una sola palabra con input().
palabra = input("Introduce una palabra: ")

if not palabra or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
    raise SystemExit
#Comprobación
# Normaliza la palabra introducida con norm(...).
# Comprueba si pertenece al conjunto bad cargado con el bloque proporcionado.
palabra_normalizada= norm(palabra)
if palabra in bad:
    print("NO CORRECTA")
else:
    print("CORRECTA")
