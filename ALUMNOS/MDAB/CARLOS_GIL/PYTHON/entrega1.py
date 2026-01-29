#EJERCICIO 1

Edem = "Marina de Empresas 2025"
print(Edem)
print(f"Tiene {len(Edem)} letras, y empieza por la letra {Edem[0]}")

#EJERCICIO 2

festivo = True
if festivo:
    print("Hoy es fiesta, voy a echarme una siesta")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) ")

#EJERCICIO 4

def ultimoCaracter(valor):
    if valor.isdigit():
        return 'Debo ser ejecutada con un string'
    return valor[-1] if valor else ''

texto = input("Introduce una palabra: ")
print(ultimoCaracter(texto))

#EJERICIO 5 -- BAD WORDS

import sys
import os

def norm(s: str) -> str:
    """Convierte un string a minúsculas y quita espacios iniciales/finales."""
    return s.strip().lower()

bad = set()
try:
    with open("bad_words.txt", encoding="utf-8") as f:
        for line in f:
            if '#' in line:
                line = line[:line.find('#')]                
            w = line.strip()
            if w:
                bad.add(norm(w))
except FileNotFoundError:
    
    sys.stderr.write("Error: El archivo 'bad_words.txt' no se encontró.\n")
    sys.exit(1)

palabra_entrada = input("No insultes: ")

if not palabra_entrada or ' ' in palabra_entrada:
    print("Introduce una sola palabra (sin espacios).")
    sys.exit(0) 
palabra_normalizada = norm(palabra_entrada)

if palabra_normalizada in bad:
    print("NO CORRECTA")
else:
    print("CORRECTA")