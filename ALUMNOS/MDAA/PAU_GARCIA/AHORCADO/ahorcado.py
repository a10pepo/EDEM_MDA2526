import sys
import os
import psycopg
import requests
import time
from collections import Counter

palabras_file = sys.argv[1]
in_order_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z']
most_freq_list = [
    "e", "a", "o", "s", "r", "n", "i", "d", "l", 
    "c", "t", "u", "m", "p", "b", "g", "v", "y", 
    "q", "h", "f", "z", "j", "ñ", "x", "k", "w"]
lista = most_freq_list

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
#CURSOR
cur = connection.cursor()
reemplazos = str.maketrans("áéíóúÁÉÍÓÚüÜ", "aeiouAEIOUuU")
palabras_file = sys.argv[1]
def normalizar(s) :
    if s is None:
        return s
    return s.strip().lower().translate(reemplazos)
def ahorcado() :
    if os.getenv("GETAPI") == "True" :
        print(os.getenv("GETAPI"))
        req = requests.get("https://rae-api.com/api/random")
        word = req.json()["data"]["word"].lower()
        word = normalizar(word)
        file = "palabrasrae.txt"
        with open(file, "w") as f:
            f.write(word)
    else : 
        file = palabras_file
        print(file)
    total = 0
    with open(file, "r+") as archivo :
        for linea in archivo:
            line = linea.strip().lower()
            count = len(line)
            print(linea, flush=True)
            acertadas = ''
            falladas = ''
            for letra in lista:
                if letra in line: 
                    acertadas += letra
                    count = count - line.count(letra)
                    print(letra + " acertada")
                else : 
                    falladas += letra
                    print(letra + " fallada")
                total = total +1
                query = """INSERT INTO ahorcado (palabra,letras_adivinadas,
                    letras_falladas,intentos) VALUES (%s,%s,%s,%s);"""
                cur.execute(query,(line,acertadas, falladas, total))
                connection.commit()
                if count <= 0 : break
    print(total)
def createtable():
        cur.execute("DROP TABLE IF EXISTS ahorcado")
        cur.execute("""CREATE TABLE IF NOT EXISTS ahorcado (
        palabra VARCHAR(100) NOT NULL,
        letras_adivinadas VARCHAR(100) DEFAULT '',
        letras_falladas VARCHAR(100) DEFAULT '',
        intentos INT DEFAULT 0,
        tiempo TIMESTAMP DEFAULT CURRENT_TIMESTAMP    
        );""")
        connection.commit()
        print("tabla creada")

def ahorcadoplus() :
    if os.getenv("GETAPI") == "True" :
        print(os.getenv("GETAPI"))
        req = requests.get("https://rae-api.com/api/random")
        word = req.json()["data"]["word"].lower()
        normalizar(word)
        file = "palabrasrae.txt"
        with open(file, "w") as f:
            f.write(word)
    else : file = palabras_file
    print(file)
    total = 0
    with open(file, "r+") as archivo :
        for linea in archivo:
            line = normalizar(linea.strip().lower())
            print(line)
            lon = len(line)
            count = lon
            print(linea, flush=True)
            acertadas = ''
            falladas = ''
            letra = 'e'
            patron = ""
            i = 0
            while (i != count) :
                patron += "_"
                i += 1
            while (count != 0) :
                patron = actualizar_patron(patron,line,letra)
                query = """SELECT palabra FROM rae WHERE LENGTH(palabra) = %s 
                        AND palabra LIKE %s; """
                cur.execute(query,(lon, patron))
                palabras = [row[0] for row in cur.fetchall()]
                palabras_fin = ""
                tried_letters = acertadas + falladas
                for palabra in palabras:
                    for letra in palabra:
                        if not(letra in tried_letters):
                            palabras_fin += letra
                letra = masComun(palabras)
                print(count)
                if letra in line:
                    acertadas += letra
                    count = count - line.count(letra)
                    print (letra + " acertada")
                else : 
                    falladas += letra
                    print (letra + " fallada")
                total = total +1
                query = """INSERT INTO ahorcado (palabra,letras_adivinadas,
                        letras_falladas,intentos) VALUES (%s,%s,%s,%s);"""
                cur.execute(query,(line,acertadas, falladas, total))
                connection.commit()
                if count <= 0 : break
    print(total)

def actualizar_patron(patron_actual, palabra_real, letra):
    letra = letra.lower()
    nuevo = ""
    for p, w in zip(patron_actual, palabra_real):
        if p != "_":
            nuevo += p
        elif w.lower() == letra:
            nuevo += w
        else:
            nuevo += "_"
    return nuevo

def masComun(palabras) :
    contador = Counter("".join(palabras))
    letra_mas_comun = contador.most_common(1)[0][0]
    return letra_mas_comun

createtable()
ahorcado()
ahorcadoplus()