import time
from datetime import datetime
import random

def adivinar_palabra(palabra):
    abecedario = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    letras_acertadas = set()
    letras_falladas = set()
    intentos = 0

    for letra in abecedario:
        intentos += 1
        if letra in palabra:
            letras_acertadas.add(letra)
            if all(l in letras_acertadas for l in set(palabra)):
                break
        else:
            letras_falladas.add(letra)

    return {
        "palabra": palabra,
        "letras_acertadas": "".join(sorted(letras_acertadas)),
        "letras_falladas": "".join(sorted(letras_falladas)),
        "intentos": intentos,
        "tiempo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Simulamos la API con una lista de palabras
def obtener_palabra_api():
    palabras_simuladas = ["ELEFANTE", "ORDENADOR", "PROGRAMACION", "PYTHON", "AHORCADO"]
    return random.choice(palabras_simuladas)

def main_local():
    resultados = []
    try:
        with open("palabras.txt", encoding="utf-8") as f:
            palabras = [line.strip().upper() for line in f if line.strip()]
    except FileNotFoundError:
        palabras = []

    for palabra in palabras:
        resultado = adivinar_palabra(palabra)
        resultados.append(resultado)

    print("palabra\tletras_acertadas\tletras_falladas\tintentos\ttiempo")
    for r in resultados:
        print(f"{r['palabra']}\t{r['letras_acertadas']}\t{r['letras_falladas']}\t{r['intentos']}\t{r['tiempo']}")

def main_api_loop():
    print("Iniciando bucle de palabras simuladas (cada 10 segundos)...")
    while True:
        palabra_api = obtener_palabra_api()
        if palabra_api:
            resultado = adivinar_palabra(palabra_api)
            print(f"{resultado['palabra']}\t{resultado['letras_acertadas']}\t{resultado['letras_falladas']}\t{resultado['intentos']}\t{resultado['tiempo']}")
        else:
            print("No se obtuvo palabra de la API.")
        time.sleep(10)

if __name__ == "__main__":
    main_local()
    main_api_loop()
