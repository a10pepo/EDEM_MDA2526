print("\n------------------------")
print("------EJERCICIO 1------")
print("------------------------\n")

mde = "Marina de Empresas 2025"

print(f"La longitud de la variable es: {len(mde)}\n" 
f"La primera letra es: {mde[0]}\n")

print("------------------------")
print("------EJERCICIO 2-------")
print("------------------------\n")

festivo = False

if festivo == True:
    print(f"Hoy es fiesta voy a echarme una siesta\n")
else:
    print(f"No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :) \n")

print("------------------------")
print("------EJERCICIO 3-------")
print("------------------------\n")


def ultimoCaracter (cadena:str):
    if type(cadena) != str:
        return "Debo ser ejectada con string. Vuelve a llamar a la función\n"
    else:
        return f"El último carácter de la cadena es: {cadena[-1]}\n"


print(ultimoCaracter("miau"))
print(ultimoCaracter(1))


print("------------------------")
print("EJERCICIO 4 -- BAD WORDS")
print("------------------------\n")

#import unicodedata (si hubiera que tener en cuenta también posibles tildes)
def norm (s:str) -> str:
    if not s or " " in s:
        print("\nIntroduce una sola palabra (sin espacios).\n")
        exit()
    else:
        minuscula = s.lower()
        final_sin_acentos= minuscula.strip()
        #sin_acentos = ''.join(
        #c for c in unicodedata.normalize('NFD', s)
        #if not unicodedata.combining(c))
        return final_sin_acentos

bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

palabra = input("Introduce una sola palabra: ")
try:
    n = norm(palabra)
    if n in bad:
        print("\nNO CORRECTA\n")
    else:
        print("\nCORRECTA\n")
except ValueError:
    print("")