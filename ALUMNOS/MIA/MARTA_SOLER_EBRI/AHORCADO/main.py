from datetime import datetime
import string
import os, psycopg
import requests
import time
import pandas as pd

def abrir_archivo(archivo):
    conjunto_palabras=[]
    with open(archivo, encoding="utf-8") as arch:
        for linea in arch:
            palabra_original=linea.strip()
            if palabra_original:
                conjunto_palabras.append(normalizar_palabra(palabra_original))
    return conjunto_palabras

def normalizar_palabra(palabra):
    palabra=palabra.strip().upper()
    palabra=palabra.replace(" ", "")
    palabra=palabra.replace('́', "")
    palabra=palabra.replace('-', "")
    palabra=palabra.replace('‒', "")
    palabra=palabra.replace('(', "")
    palabra=palabra.replace(')', "")
    palabra=palabra.replace('/', "")
    palabra=palabra.replace(':', "")
    palabra=palabra.replace("á", "a")
    palabra=palabra.replace("é", "e")
    palabra=palabra.replace("í", "i")
    palabra=palabra.replace("ó", "o")
    palabra=palabra.replace("ú", "u")
    palabra=palabra.replace("ü", "u")
    palabra=palabra.replace("è", "e")
    return palabra

def concatenar_elementos(elementos):
    resultado=""
    for elemento in elementos:
        resultado+=elemento
    return resultado

def ordenar_por_frecuencia(palabras):
    texto=concatenar_elementos(palabras)
    contador_letras={} 
    for letra in texto: 
        if letra in contador_letras:
            contador_letras[letra]+=1
        else:
            contador_letras[letra]=1
    letras_ordenadas=[]
    while contador_letras:
        frecuencia_max=-1
        for letra, frecuencia in contador_letras.items():
            if frecuencia > frecuencia_max:
                frecuencia_max=frecuencia
                letra_max=letra
            elif frecuencia == frecuencia_max:
                if letra < letra_max:
                    letra_max=letra
        letras_ordenadas.append((letra_max, frecuencia_max))
        del contador_letras[letra_max]
    return dict(letras_ordenadas)

def ahorcado_fuerza_bruta(palabras_adivinar,alfabeto):
    intentos_por_palabra=[]
    registros_totales=[]
    for palabra_adivinar in palabras_adivinar:
        intentos_en_palabra=0
        letras_acertadas=[]
        letras_falladas=[]
        letras_requeridas=set(palabra_adivinar) 
        for letra in alfabeto:
            if not letras_requeridas:  
                break
            intentos_en_palabra+=1
            if letra in palabra_adivinar:
                letras_acertadas.append(letra)
                letras_requeridas.remove(letra)
            else:
                letras_falladas.append(letra)
            registro_intento={
                "palabra": palabra_adivinar,
                "letras_acertadas": ''.join(letras_acertadas),
                "letras_falladas": ''.join(letras_falladas),
                "intentos": intentos_en_palabra,
                "tiempo": datetime.now() 
            }
            registros_totales.append(registro_intento)
        intentos_por_palabra.append(intentos_en_palabra)
    total_intentos=sum(intentos_por_palabra)
    return registros_totales, total_intentos

def ahorcado_optimizado(palabras_adivinar, palabras_rae):
    intentos_por_palabra=[]
    registros_totales=[]
    for palabra_adivinar in palabras_adivinar:
        intentos_en_palabra=0
        letras_acertadas=set()
        letras_falladas=set()
        letras_restantes=set(palabra_adivinar)
        candidatas_rae=[]
        for palabra_rae in palabras_rae:
            if len(palabra_rae) == len(palabra_adivinar):
                candidatas_rae.append(palabra_rae)       
        while letras_restantes:
            if not letras_acertadas and not letras_falladas:
                intentos_en_palabra+=1
                letra="A"               
                if letra in palabra_adivinar:
                    letras_acertadas.add(letra)
                    letras_restantes.discard(letra)
                else:
                    letras_falladas.add(letra)               
                nuevas_candidatas=[]
                for candidata in candidatas_rae:
                    if letra in letras_acertadas:
                        if letra in candidata:
                            nuevas_candidatas.append(candidata)
                    else:  
                        if letra not in candidata:
                            nuevas_candidatas.append(candidata)
                candidatas_rae=nuevas_candidatas
            else:
                if not letras_restantes:
                    break
                frecuencias=ordenar_por_frecuencia(candidatas_rae)                
                for letra in frecuencias.keys():
                    if letra not in letras_acertadas and letra not in letras_falladas:
                        letra_optima=letra
                        break
                intentos_en_palabra+=1                
                if letra_optima in letras_restantes:
                    letras_acertadas.add(letra_optima)
                    letras_restantes.discard(letra_optima)
                else:
                    letras_falladas.add(letra_optima)                
                nuevas_candidatas=[]
                for candidata in candidatas_rae:
                    if letra in letras_acertadas:
                        if letra in candidata:
                            nuevas_candidatas.append(candidata)
                    else:  
                        if letra not in candidata:
                            nuevas_candidatas.append(candidata)
                candidatas_rae=nuevas_candidatas     
            registro_intento={
                "palabra": palabra_adivinar,
                "letras_acertadas": concatenar_elementos(letras_acertadas),
                "letras_falladas": concatenar_elementos(letras_falladas),
                "intentos": intentos_en_palabra,
                "tiempo": datetime.now() 
            }
            registros_totales.append(registro_intento)  
        intentos_por_palabra.append(intentos_en_palabra)   
    total_intentos=sum(intentos_por_palabra)
    return registros_totales, total_intentos

def createTable():
  try:
    query="""
    CREATE TABLE IF NOT EXISTS palabras(
        id SERIAL PRIMARY KEY,
        palabra TEXT,
        letras_acertadas TEXT,
        letras_falladas TEXT,
        intentos INTEGER,
        tiempo TIMESTAMP
    );
    """
    cur.execute(query)
  except Exception as e:
    print(f"Error: {e}")

def insertPalabras(resultados):
  try:
      for i in range(0,len(resultados)):
        resultado=resultados[i]
        query="""
        INSERT INTO palabras (
          palabra, letras_acertadas, letras_falladas, intentos, tiempo
        )
        VALUES (%s, %s, %s, %s, %s)
        """
        values=(
          resultado["palabra"],
          resultado["letras_acertadas"],
          resultado["letras_falladas"],
          resultado["intentos"],
          resultado["tiempo"],
        )
        cur.execute(query, values)
  except Exception as e:
      print(f"Error {e}.")

def getPalabras():
    query="SELECT * FROM palabras;"
    df=pd.read_sql_query(query, connection)
    print(df.to_string(index=False))

def getDiferenciaTiempo():
    query="""
    SELECT
        MIN(tiempo) AS tiempo_inicial,
        MAX(tiempo) AS tiempo_final,
        MAX(tiempo) - MIN(tiempo) AS diferencia
    FROM
        palabras;
    """
    df=pd.read_sql_query(query, connection)
    return df.to_string(index=False)

def deletePalabras():
    query="TRUNCATE palabras RESTART IDENTITY;"
    cur.execute(query)

PALABRAS_ADIVINAR=abrir_archivo("ahorcado.txt")
PALABRAS_RAE=abrir_archivo("diccionario.txt")
ABECEDARIO=string.ascii_uppercase+"Ñ"

url=os.getenv("DATABASE_URL")
connection=psycopg.connect(url)
cur=connection.cursor()

is_api=os.environ.get("is_api")

createTable()
deletePalabras()

if is_api=="True":
    while True:
        response=requests.get("https://rae-api.com/api/random")
        data=response.json()
        palabra_api=[data['data']['word'].upper()]
        resultados=ahorcado_fuerza_bruta(palabra_api, ABECEDARIO)
        insertPalabras(resultados)
        getPalabras()
        connection.commit()
        time.sleep(10)
else:
   (resultados_fuerza_bruta, intentos_fuerza_bruta)=ahorcado_fuerza_bruta(PALABRAS_ADIVINAR, ABECEDARIO)
   insertPalabras(resultados_fuerza_bruta)
   print(f"Tiempos del ahorcado a fuerza bruta: \n {getDiferenciaTiempo()}")
   print(f"Intentos del ahorcado a fuerza bruta: {intentos_fuerza_bruta}")
   (resultados_optimizado, intentos_optimizado)=ahorcado_optimizado(PALABRAS_ADIVINAR, PALABRAS_RAE)
   insertPalabras(resultados_optimizado)
   print(f"Tiempos del ahorcado optimizado: \n {getDiferenciaTiempo()}")
   print(f"Intentos del ahorcado optimizado: {intentos_optimizado}")

getPalabras()

connection.commit()

cur.close()
connection.close()