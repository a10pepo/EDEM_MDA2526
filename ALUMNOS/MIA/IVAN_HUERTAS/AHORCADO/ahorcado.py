import sys
import string
import os

def adivinar_palabra_por_fuerza_bruta(palabra_objetivo):
    
    palabraminuscula = palabra_objetivo.lower()
    
    letras_a_descubrir = set(c for c in palabraminuscula if 'a' <= c <= 'z')
    
    intentos_totales = 0
    letras_descubiertas = set()

    for letra in string.ascii_lowercase:
        
        intentos_totales += 1
        
        if letra in palabraminuscula:
            letras_descubiertas.add(letra)
            
        if letras_descubiertas == letras_a_descubrir:
            return intentos_totales
            
    return intentos_totales

def ejecutar_ahorcado(nombre_archivo):
    
    try:
        os.path.exists(nombre_archivo)
    except:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        

    total_intentos_global = 0
    palabras = []

    try:
        with open(nombre_archivo, 'r') as f:
            palabras = [linea.strip() for linea in f if linea.strip()] 
            
    except:
        print("Error al leer el archivo")
        

    print("adivinando palabras")
    
    for palabra in palabras:
        if not palabra:
            continue
            
        intentos = adivinar_palabra_por_fuerza_bruta(palabra)
        total_intentos_global += intentos
        
        print(f"Palabra: {palabra.ljust(15)}  Intentos: {intentos}")

    print("--- Total ---")
    print(f" Suma de todos los intentos: {total_intentos_global}")

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Uso: python ahorcado.py <nombre_del_archivo.txt>")
        sys.exit(1)
    
    nombre_archivo = sys.argv[1]
    ejecutar_ahorcado(nombre_archivo)