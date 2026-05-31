import os, psycopg

# URL CONEXIÓN A BD
url = os.getenv("DATABASE_URL")
# CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")


def createUser():
    try:
        query = """INSERT INTO users (first_name, last_name, email, password) 
        VALUES ('Miguel','Herrera','miki@example.com','123456');"""
        cur.execute(query)
        print("Usuario creado")
    except:
        print("Error creando usuario")


createUser()
connection.commit()
