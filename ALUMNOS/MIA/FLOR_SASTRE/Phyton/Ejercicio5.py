#Escribe un programa que pida una palabra por teclado y diga si está en la lista de palabras prohibidas 
# (bad_words.txt). La comparación debe ser insensible a mayúsculas .
#Material proporcionado (NO modificar)
#Se guarda el bloque que carga bad_words.txt en un set llamado bad (una palabra por línea):


#normalizacion y convierte minusculas, sin espacios
def norm(s: str) -> str:
    return s.lower().strip()

#cargo archivo
bad = set()
with open("bad_words.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            bad.add(norm(w))

#pido palabra
palabra = input("Introduce una palabra: ")

#sihay espacios o vacia
if not palabra or " " in palabra:
    print("Introduce una sola palabra (sin espacios).")
    exit()

palabra_normalizada = norm(palabra)
if palabra_normalizada in bad:
    print("NO CORRECTA")
else:
    print("CORRECTA")
