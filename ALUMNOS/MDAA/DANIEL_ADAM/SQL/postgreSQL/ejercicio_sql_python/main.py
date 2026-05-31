import os, psycopg

try:
 #URL CONEXIÓN A BD 
 url = os.getenv("DATABASE_URL")
 #CONEXIÓN A BD
 connection = psycopg.connect(url)
 # Cursor
 cur = connection.cursor()
 print("BD conectada con éxito")
except:
 print("Error conectando a la BD")


