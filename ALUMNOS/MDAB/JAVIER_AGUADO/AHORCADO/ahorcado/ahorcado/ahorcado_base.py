import sys

def main():
    archivo = sys.argv[1] # Leemos el archivos palabras.txt como segundo argumento
    with open(archivo, "r", encoding="utf-8") as f: # Abrimos el fichero en modo lectura
        palabras = f.readlines() # Guardamos en "palabras" las lineas del fichero
            
    total_intentos = 0 # Inicializamos el contador de intentos totales

    print("Resultados del juego del ahorcado:")

    for palabra in palabras: # Recorremos todas nuestras palabras para intentar adivinarlas
        palabra = palabra.strip() # A cada linea le aplicamos el .strip() que elimina saltos de línea, dejando solamente la palabra
        letras_palabra = set(palabra) # Creamos un set de la palabra para saber cuántas letras únicas tiene (por si se repiten letras en la misma palabra)
        letras_acertadas = set() # Inicializamos un set donde guardaremos las letras que acertemos
        letras_falladas = set() # Inicializamos un set para las letras falladas
        intentos = 0  # Inicializamos los intentos para esta palabra
        for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ": # Recorremos todas las letras del abc
            intentos += 1 # Añadimos un intento por cada letras que probamos
            if letra in letras_palabra: # Si esa letra está en nuestra palabra
                letras_acertadas.add(letra) # La añadimos al set de letras acertadas
            else:
                letras_falladas.add(letra) # Si no está, la añadimos a las falladas
            if letras_acertadas == letras_palabra: # Si ya hemos acertado todas la letras, es decir, nuestros set de letras de la palabra es igual que el set de letras acertadas
                break # Terminamos el bucle de búsqueda de letras porque ya hemos acertado la palabra

        total_intentos += intentos # Sumamos los intentos de esta palabra al contador de intentos total

        print(f"Palabra: {palabra} - Intentos: {intentos}")

    print("Suma total de intentos:", total_intentos)
    
if __name__ == "__main__":
    main()