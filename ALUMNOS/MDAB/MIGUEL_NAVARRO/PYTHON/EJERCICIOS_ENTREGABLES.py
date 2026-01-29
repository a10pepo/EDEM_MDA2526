print("EJERCICIOS ENTREGABLES - PYTHON (1)")


print("\nEjercicio 1")
var1 = "Marina de Empresas 2025"    # defino la variable string
print(f"La variable '{var1}' tiene {len(var1)} caracteres.")    # longitud de la variable
print(f"La primera letra es la '{var1[0]}'")    # primera letra


print("\nEjercicio 2")
festivo = False # variable "festivo" de tipo Booleano
if festivo == True:
    print("Hoy es fiesta, voy a echarme una siesta!!")
else:
    print("No es fiesta pero no pasa nada porque tengo que hacer el entregable de Python :)")


print("\nEjercicio 3")
def ultimoCaracter(cadena: str):
    """
    Recibe un string y devuelve el último carácter de la misma en un nuevo string
    Args: string
    Returns: string: última letra del string recibido
    """
    if isinstance(cadena, str):
        print(f"'{cadena[-1]}' es el último carácter")
    else:
        print("Debo ser ejecutada con un string")
ultimoCaracter("Python")    # llamo a la función


print("\nEjercicio 4 - Bad Words")

def norm(s: str):
    """
    Convierte un string a minúsculas y elimina los espacios al inicio y al final de la misma
    Args: string
    Returns: string en minúsculas y sin espacios al inicio y al final
    """
    return s.strip().lower()

bad = set()         # guarda el bloque que carga "bad_words.txt" en un set llamado bad con una palabra por línea
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

word = input("Introduce una sola palabra. ")    # Pide una palabra
if (" " in word) or (word == ""):   # Comprueba que la entrada no está vacía no tiene espacios
    print("Introduce una sola palabra (sin espacios).")
else:
    word = norm(word)               # Normaliza la palabra introducida
    if word in bad:                 # Comprueba si pertenece al conjutno bad
        print("NO CORRECTA")
    else:
        print("CORRECTA")