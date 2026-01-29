import os, psycopg
#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")

def getUsers():
    query = "SELECT * FROM users;"
    cur.execute(query)
    print("Nuestros usuarios:",cur.fetchall())

getUsers()


def createUser():
    try:
        query = """INSERT INTO users (first_name, last_name, email, password) 
        VALUES ('Miguel','Herrera','miki@example.com','123456');"""
        cur.execute(query)
        print("Usuario creado")
    except:
        print('Error creando usuario')
createUser()
connection.commit()

# NUEVA FUNCIÓN PARA CREAR USUARIO PASANDO PARÁMETROS
def createUser(first_name, last_name, email, password):
    try:
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (first_name, last_name, email, password))
        connection.commit()
        print("Usuario creado")
    except Exception as e:
        print("Error creando usuario:", e)
createUser("Eusebio","García","eusebio@gmail.com","123456")
connection.commit()
