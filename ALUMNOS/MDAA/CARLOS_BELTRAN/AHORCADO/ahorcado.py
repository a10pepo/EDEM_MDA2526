import sys, psycopg, os, requests, time, datetime

def getWordList():
    lista=[]

    if os.getenv("GETWORDFROMAPI"):
        req= requests.get("https://rae-api.com/api/random")
        palabraRAE= req.json()["data"]["word"].upper()
        lista.append(palabraRAE)
    else:
        filename= sys.argv[1]
        for lines in open(filename, "r", encoding="utf-8"):
            lista.append(lines.strip().upper())
    return lista

url = os.getenv("DATABASE_URL")
connection = psycopg.connect(url)
cur = connection.cursor()

while True:
    lista = getWordList()

    letters="EAOSNRILDCTUMPBGVQHFYJKWZXÑÁÉÓÍÚ"

    try:
        letrasProbadas=0

        for palabra in lista:
            letrasAcertadas=""
            letrasFalladas=""
            palabraAComparar=palabra
            for letter in letters:
                timestamp_actual = datetime.datetime.now()
                if palabraAComparar=="":
                    break

                letrasProbadas+=1

                if letter in palabraAComparar:
                    letrasAcertadas+=letter
                    palabraAComparar = palabraAComparar.replace(letter, "")
                else:
                    letrasFalladas+=letter

                cur.execute(
                    """INSERT INTO juego_palabras (palabra, letras_acertadas, letras_falladas, intentos, tiempo) 
                    VALUES (%s, %s, %s, %s, %s)""",
                    (palabra, letrasAcertadas, letrasFalladas, letrasProbadas, timestamp_actual))

        connection.commit()
        timeToComplete = cur.execute(f"SELECT EXTRACT(EPOCH FROM (SELECT MAX(tiempo) FROM juego_palabras WHERE palabra='{palabra}')::TIMESTAMP - (SELECT MIN(tiempo) FROM juego_palabras WHERE palabra='{palabra}')::TIMESTAMP)")

        print(f"Palabra: {palabra}",flush=True)
        print(f"Letras probadas final: {letrasProbadas}",flush=True)
        print(f"Aciertos: {letrasAcertadas}",flush=True)
        result = timeToComplete.fetchone()

        seconds = float(result[0])
        print(f"Tiempo para completar el ahorcado: {seconds} segundos",flush=True)


        time.sleep(1)
    except Exception as e:
        print(e.with_traceback())

cur.close()
connection.close()