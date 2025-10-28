intentos=0
letras = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", 
    "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", 
    "U", "V", "W", "X", "Y", "Z"
]

palabras = []
with open("palabras.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        palabras.append(linea.strip())


intentos = 0
letras = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", 
    "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", 
    "U", "V", "W", "X", "Y", "Z"
]

palabras = []
with open("palabras.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        palabras.append(linea.strip().upper())

for palabra in palabras:
    huecos = len(palabra)
    
    for letra in letras:
        intentos += 1
        if letra in palabra:
            
            apariciones = palabra.count(letra)
            huecos -= apariciones
            
        if huecos <= 0:
            break  

print(intentos)
