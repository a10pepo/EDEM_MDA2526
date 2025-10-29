import sys
import os
import psycopg
import requests
import time

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

def ahorcado() :
    if os.getenv("GETAPI") == "True" :
        print(os.getenv("GETAPI"))
        req = requests.get("https://rae-api.com/api/random")
        word = req.json()["data"]["word"].lower()
        reemplazos = str.maketrans("áéíóúÁÉÍÓÚüÜ", "aeiouAEIOUuU")
        word = word.translate(reemplazos)
        file = "palabrasrae.txt"
        with open(file, "w") as f:
            f.write(word)
    else : file = palabras_file
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
                if count == 0 : break
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

def ahorcadoplus() :
    if os.getenv("GETAPI") == "True" :
        print(os.getenv("GETAPI"))
        req = requests.get("https://rae-api.com/api/random")
        word = req.json()["data"]["word"].lower()
        file = "palabrasrae.txt"
        with open(file, "w") as f:
            f.write(word)
    else : file = palabras_file
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
                else : 
                    falladas += letra
                total = total +1
                query = """INSERT INTO ahorcado (palabra,letras_adivinadas,
                    letras_falladas,intentos) VALUES (%s,%s,%s,%s);"""
                cur.execute(query,(line,acertadas, falladas, total))
                connection.commit()
                if count == 0 : break
    print(total)

createtable()
ahorcado()

while (True) :
    ahorcado()
    time.sleep(10)