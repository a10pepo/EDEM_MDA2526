# --- IMPORTAR LIBRERIAS --- #
import os
import psycopg as ps
import requests as rq
import string
import time

# --- NORMALIZAR PALABRAS ---
def norm(s: str) -> str:
    return s.upper().strip()

# --- ABRIR .TXT CON PALABRAS ESTÁTICAS --- #
palabras = []
with open("palabras.txt", encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            palabras.append(norm(w))


# --- CONFIGURACIÓN  DE VARIABLES GLOBABLES---
abecedario_alfabetico = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
contador_alfabetico = 0
url = os.getenv("DATABASE_URL")


# OPTIMIZACION (FREQ % RELATIVA LETRAS EN LEXICO)
# FUENTE: https://es.wikipedia.org/wiki/Frecuencia_de_aparici%C3%B3n_de_letras
frecuencias_es = {'A': 12.53, 'B': 1.42,'C': 4.68,'D': 5.86,'E': 13.68,'F': 0.69,'G': 1.01,'H': 0.70,
                'I': 6.25,'J': 0.44,'K': 0.01,'L': 4.97,'M': 3.15,'N': 6.71,'Ñ': 0.31,'O': 8.68,'P': 2.51,
                'Q': 0.88,'R': 6.87,'S': 7.98,'T': 4.63,'U': 3.93,'V': 0.90,'W': 0.02,'X': 0.22,'Y': 0.90,'Z': 0.52 }
abecedario_ordenado = sorted(frecuencias_es, key=frecuencias_es.get, reverse=True)
contador_ordenado = 0


# --- CONEXIÓN A LA BD ---
try:
    connection = ps.connect(url)
    cur = connection.cursor()
    print("BD conectada con éxito")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS resultados_ahorcado(
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        palabra TEXT NOT NULL,
        letras_acertadas TEXT NOT NULL,
        letras_falladas TEXT,
        intentos INT,
        tiempo TIMESTAMP NOT NULL DEFAULT now()); """)
    connection.commit()
    print("Tabla 'resultados_ahorcado' creada o ya existía")

except Exception as e:
    print("Error conectando a la BD:", e)
    exit(1)


# # --- FUNCIÓN DE INSERCIÓN ---
def insertar_resultado(palabra, letras_ok, letras_fail, intentos):
    cur.execute("""
        INSERT INTO resultados_ahorcado (palabra, letras_acertadas, letras_falladas, intentos)
        VALUES (%s, %s, %s, %s);
    """, (palabra, ''.join(letras_ok), ''.join(letras_fail), intentos))
    connection.commit()


# --- FUNCIÓN PRINCIPAL DEL JUEGO ---
def resolver_palabra(palabra,abecedario):
    global contador_alfabetico
    global contador_ordenado 
    registro = list(palabra)
    letras_acertadas = []
    letras_falladas = []

    if abecedario == abecedario_alfabetico:
        while registro:
            for letra in abecedario:
                contador_alfabetico += 1
                if letra in registro:
                    while letra in registro:
                        letras_acertadas.append(letra)
                        registro.remove(letra)
                    if not registro:
                        break
                else:
                    letras_falladas.append(letra)
            if not registro:
                break
    else:
        while registro:
            for letra in abecedario:
                contador_ordenado += 1
                if letra in registro:
                    while letra in registro:
                        letras_acertadas.append(letra)
                        registro.remove(letra)
                    if not registro:
                        break
                else:
                    letras_falladas.append(letra)
            if not registro:
                break
        insertar_resultado(palabra, letras_acertadas, letras_falladas, contador_ordenado)

# --- PROCESAR PALABRAS.TXT ---
for palabra in palabras:
    resolver_palabra(palabra,abecedario_alfabetico)

for palabra in palabras:
    resolver_palabra(palabra,abecedario_ordenado)


# --- COMPARACIÓN ENTRE MÉTODOS ---

def comparacion_txt(palabras,intentos_alfa,intentos_opt):
    
    # COMPARACION INTENTOS MEDIOS POR PALABRA
    total_palabras = len(palabras)

    media_intentos_alfa = round(intentos_alfa/total_palabras,2)
    media_intentos_opt = round(intentos_opt/total_palabras,2)

    reducc_intentos = round(((media_intentos_alfa -media_intentos_opt) /media_intentos_alfa) * 100,2)

    # COMPARACION INTENTOS MEDIOS POR LETRA
    total_letras = sum(len(p) for p in palabras)
    
    intentos_letra_alfa = round(intentos_alfa/total_letras,2)
    intentos_letra_opt = round(intentos_opt/total_letras,2)

    return f"""Comparación entre métodos en las palabras del archivo .txt:

    Intentos medios por palabra:
    Método alfabético: {media_intentos_alfa}  
    Método optimizado: {media_intentos_opt}
    
    Intentos medios por letra:
    Método alfábetico: {intentos_letra_alfa}
    Método optimizado: {intentos_letra_opt}
    
    Reducción de intentos con optimización: {reducc_intentos} %"""


print(comparacion_txt(palabras, contador_alfabetico,contador_ordenado),flush=True)
palabras.clear()

# --- PEDIR PALABRAS A LA API ---
for _ in range(10):
    try: 
        url = "https://rae-api.com/api/random"
        headers = {"Accept": "application/json"}
        response = rq.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            palabra = data["data"]["word"].upper()
            resolver_palabra(palabra,abecedario_ordenado)
        else:
            print("Error al obtener palabra de la API:", response.status_code,flush=True)
    except Exception as e:
        print("Error al conectar con la API:", e,flush=True)
        continue

    time.sleep(10)

