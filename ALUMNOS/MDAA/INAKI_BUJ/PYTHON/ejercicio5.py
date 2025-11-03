##Función de normalización
def norm(s:str) -> str:
    return s.strip().lower()

##Cargar el archivo de palabras prohibidas
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))
            
##Pedir al usuario la palabra
palabra = input("Introduzca una palabra: ")

##Validación
if not palabra or " " in palabra.strip():
    print("Introduce una sola palabra (sin espacios).")
    
else:
    palabra_norm = norm(palabra)
    if palabra_norm in bad:
        print("NO CORRECTA")
    else:
        print("CORRECTA")
