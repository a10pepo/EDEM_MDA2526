import os, psycopg

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")

def getUsers():
   query = "SELECT * FROM employers;"
   cur.execute(query)
   print("Nuestros usuarios:",cur.fetchall())
getUsers()
