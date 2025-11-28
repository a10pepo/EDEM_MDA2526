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
palabras_file = sys.argv[1]
# Crea la tabla de ahorcado con palabra, acertadas, falladas, intentos globales y tiempo
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

# ahorcado simple, probando desde listas con fuerza bruta
def ahorcado() :
    if os.getenv("GET_API") == "True" :
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

# ahorcado con mejoras de estrategia. Hace consultas a una db con 500k de palabras 
# y encuentra la letra más posible dado un patrón, por ejemplo para _a_a devuelve
# la letra más común que podría ocupar esos huecos
def ahorcadoplus() :
    # si la variable de entorno está activada saca palabras desde la RAE
    if os.getenv("GET_API") == "True" :
        print(os.getenv("GETAPI"))
        req = requests.get("https://rae-api.com/api/random")
        word = req.json()["data"]["word"].lower()
        normalizar(word)
        file = "palabrasrae.txt"
        with open(file, "w") as f:
            f.write(word)
    # else, lo saca desde el fichero inicializado al principio con sys.argv[1]
    else : file = palabras_file
    print(file)
    total = 0
    aciertos_totales = 0
    with open(file, "r+") as archivo :
        for linea in archivo:
            line = normalizar(linea)  # normalizar quita tildes, pone en minuscula y hace strip
            print("")
            print(f"palabra a adivinar: {line}", flush=True) # flush vacía el buffer
            lon= len(line) # lon para la query a la tabla de la rae
            count = lon # count para el bucle
            acertadas = ''
            falladas = ''
            letra = 'e' # ahorra la primera iteración (consulta muy costosa)
            patron = ""
            if "e" in line:
                acertadas += "e"
                print("acierto!")
            else :
                falladas += "e"
                print("error!")
            count = count - line.count(letra)
            print(f"faltan {count} letras")
            i = 0
            while (i != lon) : # rellena el patrón
                patron += "_"
                i += 1
            
            print(f"probando la letra {letra}...")
            while (count >= 0) :
    #actualizar_patrón cambia los guiones por las letras acertadas de ____ a -> _a_a
                patron = actualizar_patron(patron,line,letra)
                print(patron)
    # esta query busca en una db con todas las palabras de la rae y se trae todas
    # las palabras que coinciden con el patrón
    # para _a_a trae casa, cata, cama, mapa, pata...
                query = """SELECT palabra FROM rae WHERE LENGTH(palabra) = %s
                        AND palabra LIKE %s; """
                cur.execute(query,(lon, patron))
                palabras = [row[0] for row in cur.fetchall()]
                palabras_fin = ""
                # solo se incluyen palabras con letras no probadas
                tried_letters = acertadas + falladas
                for palabra in palabras: 
                    for letter in palabra:
                        if not(letter in tried_letters):
                            palabras_fin += letter
                # hay palabras de la rae no incluidas en la db pese a tener medio millón xd. 
                # (Especialmente conjugaciones de verbos)
                if palabras_fin == "" : 
                    print("activando emergencia")
                    total,count = ahorcado_emergencia(line, tried_letters,acertadas,falladas,total,count)
                    # hay palabras de la rae no incluidas en la db pese a tener medio millón xd. (Especialmente conjugaciones de verbos)
                    break
                letra = masComun(palabras_fin) # encuentra la letra más repetida
                print(f"probando letra {letra}...")
                if letra in line:
                    acertadas += letra
                    aciertos_totales += 1
                    print("acierto!")
                    count = count - line.count(letra) # resta las veces que ha acertado la letra
                    # print (letra + " acertada")
                else :
                    falladas += letra
                    print("error!")
                    # print (letra + " fallada")
                print(f"faltan {count} letras")
                total += 1
                query = """INSERT INTO ahorcado (palabra,letras_adivinadas,
                        letras_falladas,intentos) VALUES (%s,%s,%s,%s);"""
                cur.execute(query,(line,acertadas, falladas, total))
                connection.commit()
                if count <= 0 :
                    print(line)
                    break
    print(total)
    pctAcierto = round(aciertos_totales/total *100,2)
    print(f"Intentos: {total}, Aciertos: {aciertos_totales}, Porcentaje de acierto de un {pctAcierto}%")

# actualiza el patrón a adivinar dada una letra y la palabra a adivinar
# pasado _a_a, s y casa devuelve _asa
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

# Devuelve la letra más repetida en un string
def masComun(palabras) :
    if palabras == "" : return ""
    contador = Counter("".join(palabras))
    letra_mas_comun = contador.most_common(1)[0][0]
    return letra_mas_comun

# Quita tildes, diéresis, pone en minúscula y quita espacios
def normalizar(s) :
    reemplazos = str.maketrans("áéíóúÁÉÍÓÚüÜ", "aeiouAEIOUuU")
    if s is None:
        return s
    return s.strip().lower().translate(reemplazos)

# si la palabra no está registrada en db, se activa este metodo para resolverla
# con fuerza bruta utilizando la lista de letras más frecuentes
# 
def ahorcado_emergencia(line, tried_letters,acertadas,falladas, total,count) :
    for letra in most_freq_list:
        if letra not in tried_letters:
            print(f"faltan {count} letras")
            print(f"probando letra {letra}...")
            if letra in line:
                    acertadas += letra
                    count = count - line.count(letra)
                    print(f"acierto!")
            else :
                    falladas += letra
                    print("error!")
            total = total +1
            query = """INSERT INTO ahorcado (palabra,letras_adivinadas,
                    letras_falladas,intentos) VALUES (%s,%s,%s,%s);"""
            cur.execute(query,(line,acertadas, falladas, total))
            connection.commit()
            if count <= 0 : break
    print(line)
    return total, count

createtable()
if os.getenv("GET_API") == "True" :
    while(True) :
        ahorcado()
        time.sleep(5)
else : ahorcado()
if os.getenv("GET_API") == "True" :
    while(True) :
        ahorcadoplus()
        time.sleep(5)
else : ahorcadoplus()