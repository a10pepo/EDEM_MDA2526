import string
import os
import sys
import requests

ABECEDARIO = string.ascii_uppercase  # "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def ahorcado_0(fichero_palabras):
    # Diccionario para guardar los resultados
    resultados = {}

    try:
        with open(fichero_palabras, 'r', encoding='utf-8') as fichero:
            
            for linea in fichero:
                palabra = linea.strip().upper()
                letras_objetivo = set(palabra) # Las letras que contiene la palabra
                
                # Variables para esta palabra
                intentos = 0
                letras_acertadas = set()
                letras_fallidas = set() 
                
                for letra_del_abecedario in ABECEDARIO:
                    # Sumamos un intento por cada letra del abecedario que revisamos
                    intentos += 1
                    
                    # Comparamos la letra del abecedario con la palabra
                    if letra_del_abecedario in letras_objetivo:
                        letras_acertadas.add(letra_del_abecedario) # Si está, la añadimos a nuestras letras acertadas
                    else:
                        letras_fallidas.add(letra_del_abecedario) # Si no está, la añadimos a fallidas 
                    
                    # Comprobar si ya hemos encontrado todas las letras
                    if letras_acertadas == letras_objetivo:
                        break # Si hemos acertado todas, paramos de recorrer el abecedario
                
                # Guardamos el número de intentos para esa palabra en formato clave(palabra):valor(numero de intentos)
                resultados[palabra] = {
                                        "intentos": intentos,
                                        "letras_acertadas": letras_acertadas,
                                        "letras_fallidas": letras_fallidas
                                    } 

        return resultados

    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return None


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Uso: python ahorcado.py <nombre_del_fichero>")
        sys.exit(1)

    fichero_palabras = sys.argv[1]
    
    resultados_finales = ahorcado_0(fichero_palabras)
    
    if resultados_finales:
        print("--- Análisis completado ---")
        print(f"Abecedario usado: {ABECEDARIO}")
        print(f"Fichero de palabras: {fichero_palabras}\n")
        
        # Imprimimos los resultados
        for palabra, datos in resultados_finales.items():
            print(f"\nPalabra: {palabra}")
            print(f"  Intentos: {datos['intentos']}")
            print(f"  Letras acertadas: {datos['letras_acertadas']}")
            print(f"  Letras fallidas: {datos['letras_fallidas']}")
