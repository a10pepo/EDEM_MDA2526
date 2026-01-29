import string
import sys

# --- Estrategia 1: Orden Alfabético (Original) ---
abecedario_es = list(string.ascii_uppercase) 
indice_n = abecedario_es.index("N") 
abecedario_es.insert(indice_n + 1, "Ñ")


# --- Estrategia 2: Orden por Frecuencia (Óptima) ---
# Lista de letras ordenada por frecuencia de aparición en el idioma español.
# Fuente: Análisis de corpus lingüísticos del español.
ORDEN_OPTIMO_FRECUENCIA = [
    'E', 'A', 'O', 'S', 'R', 'N', 'I', 'L', 'D', 'T', 'U', 
    'C', 'M', 'P', 'B', 'G', 'V', 'H', 'F', 'Y', 'Q', 'Z', 
    'J', 'Ñ', 'X', 'K', 'W'
]


def simular_intentos(lista_de_palabras, estrategia_letras):
    """
    Ejecuta la simulación del ahorcado sobre una lista de palabras
    usando una estrategia de letras específica.
    """
    intentos_totales = 0
    
    # Iteramos sobre cada palabra que hemos cargado
    for palabra in lista_de_palabras:
        
        n_letras_restantes = len(palabra)

        # Iteramos sobre la estrategia de letras (alfabética u óptima)
        for letra in estrategia_letras:
            # Contamos un intento solo si todavía quedan letras por adivinar
            if n_letras_restantes > 0:
                intentos_totales += 1
                
                # Vemos cuántas veces aparece esta letra en la palabra
                n_aparicion = palabra.count(letra)
                
                if n_aparicion > 0:
                    # Si aparece, restamos esas letras del total
                    n_letras_restantes -= n_aparicion
                    
                    # Si ya hemos encontrado todas las letras, paramos
                    if n_letras_restantes == 0:
                        break # Salimos del bucle de letras
            else:
                break # La palabra ya fue adivinada
                
    return intentos_totales


# --- Carga y Ejecución ---

# 1. Leer todas las palabras del fichero UNA SOLA VEZ
try:
    lista_palabras = []
    with open("palabras.txt", encoding="utf-8") as doc_palabras:
        for line in doc_palabras:
            palabra = line.strip().upper() # Limpiar y pasar a mayúsculas
            if palabra: # Nos aseguramos de que no sea una línea vacía
                lista_palabras.append(palabra)
except FileNotFoundError:
    print(f"Error: No se encontró el fichero 'palabras.txt'.")
    print("Asegúrate de que el fichero esté en la misma carpeta que el script.")
    sys.exit() # Detenemos la ejecución si no hay fichero

if not lista_palabras:
    print("El fichero 'palabras.txt' está vacío. No hay nada que simular.")
    sys.exit()

print(f"Fichero leído. Se procesarán {len(lista_palabras)} palabras.")
print("--- Iniciando simulaciones... ---")


# 2. Ejecutar ambas simulaciones
intentos_alfabetico = simular_intentos(lista_palabras, abecedario_es)
intentos_optimo = simular_intentos(lista_palabras, ORDEN_OPTIMO_FRECUENCIA)


# 3. Mostrar resultados comparativos
print("\n--- RESULTADOS DE LA SIMULACIÓN ---")
print(f"Palabras analizadas: {len(lista_palabras)}\n")

print("Estrategia 1: Orden Alfabético")
print(f"   Total de intentos: {intentos_alfabetico}")
print(f"   Promedio por palabra: {intentos_alfabetico / len(lista_palabras):.2f} intentos")

print("\nEstrategia 2: Orden por Frecuencia (Óptima)")
print(f"   Total de intentos: {intentos_optimo}")
print(f"   Promedio por palabra: {intentos_optimo / len(lista_palabras):.2f} intentos")

print("\n--- CONCLUSIÓN ---")
ahorro_absoluto = intentos_alfabetico - intentos_optimo
ahorro_porcentual = (ahorro_absoluto / intentos_alfabetico) * 100
print(f"La estrategia óptima ahorró {ahorro_absoluto} intentos en total.")
print(f"Es un {ahorro_porcentual:.2f}% más eficiente.")