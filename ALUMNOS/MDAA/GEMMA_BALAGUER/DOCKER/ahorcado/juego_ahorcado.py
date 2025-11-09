import os, psycopg

def norm(s: str):
    return s.strip().lower()

#Vamos a cargar las palabras dese el archivo.
palabra=set()
import os

with open("palabra.txt",encoding="utf-8") as f:
    for line in f:
        w = line.strip()
        if w:
            palabra.add(w.lower().strip())

abecedario = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's',
    't', 'u', 'v', 'w', 'x', 'y', 'z'
]
 ################CONEXIÓN BD
url = os.getenv("DATABASE_URL")
connection = psycopg.connect(url)



