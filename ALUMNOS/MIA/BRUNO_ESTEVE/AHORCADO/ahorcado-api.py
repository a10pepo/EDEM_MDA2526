import string
import requests
import unicodedata
import time

def strip_accents(s: str) -> str:
    """Elimina los acentos de una palabra"""
    nf = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in nf if unicodedata.category(ch) != "Mn")

def get_random_word() -> str:
    """Obtiene una palabra aleatoria de la API de la RAE y la devuelve en mayúsculas sin acentos."""
    url = "https://rae-api.com/api/random"
    response = requests.get(url)
    response.raise_for_status()  # lanza excepción si hay error HTTP
    data = response.json()

    palabra = data.get('data', {}).get('word', '').upper()
    palabra = strip_accents(palabra)
    return palabra

def simulate_guess(palabra: str) -> int:
    """Simula intentar adivinar la palabra letra por letra en orden alfabético."""
    intentos = 0
    abecedario_es = list(string.ascii_uppercase)
    abecedario_es.insert(abecedario_es.index("N") + 1, "Ñ")

    n_letras_restantes = len(palabra)
    for letra in abecedario_es:
        intentos += 1
        n_aparicion = palabra.count(letra)
        n_letras_restantes -= n_aparicion
        if n_letras_restantes == 0:
            break
    return intentos

# Bucle infinito: repite cada 10 segundos
while True:
    try:
        palabra = get_random_word()
        print("\n--------------------------------")
        print(f"Palabra obtenida: {palabra}")
        intentos = simulate_guess(palabra)
        print(f"Intentos necesarios: {intentos}")
    except Exception as e:
        print(f"¡Error obteniendo palabra: {e}")

    print("Esperando 10 segundos para la siguiente palabra...\n")
    time.sleep(10)
