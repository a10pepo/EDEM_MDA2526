import os, psycopg
# Importa la biblioteca os (Operating System). 
# Esta biblioteca estándar de Python te permite interactuar con el sistema operativo, 
# y su función más común es leer "variables de entorno".
#URL CONEXIÓN A BD 
#Le pide al sistema operativo el valor de la variable de entorno que se llama DATABASE_URL
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
# No puedes enviar comandos SQL directamente con la connection.
# Necesitas un cursor que ejecuta tus 
# comandos y te devuelve los resultados.
cur = connection.cursor()
print("BD conectada con éxito")

#Creamos la tabla users para después mostrarla con el getUsers
def createTableUsers():
  try:
    query= """CREATE TABLE users (
                id INTERGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NUL);"""
    cur.execute(query)
    print("Tabla creada con éxito")
  except: 
    print("Error creando tabla")

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



