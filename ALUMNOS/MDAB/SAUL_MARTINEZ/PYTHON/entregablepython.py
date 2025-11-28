 # Ejercicio 1

variable = "Marina de empresas 2025"
print(f"La variable contiene {len(variable)} letras")
print(f"La primera letra de la variable es: {variable[0]}")

# Ejercicio 2

festivo=False
if festivo==True:
    print("Hoy es fiesta voy a echarme una siesta!!")
else: 
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ")

# Ejercicio 4

def ultimoCaracter(frase):
    if isinstance(frase, str):
        return f"El último carácter es: {frase[-1]}" 
    else:
        return "Debo ser ejecutada con un string"
print(ultimoCaracter("EDEM"))
print(ultimoCaracter(56165))

# Ejercicio 5 — Bad Words

def norm(s:str)->str:
    return s.lower().strip()
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))
palabra=input("Introduce una palabra: ")
if not palabra or " " in palabra.strip():
    print("Introduce una sola palabra (sin espacios).")
else: 
    palabra_normalizada=norm(palabra)
    if palabra_normalizada in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")