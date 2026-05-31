import os, psycopg

#URL CONEXIÓN A BD 
try:
    url = os.getenv("DATABASE_URL")

#CONEXIÓN A BD​

    connection = psycopg.connect(url)

# Cursor​

    cur = connection.cursor()

    print("BD conectada con éxito")

except Exception as e:
    print("ERROR:", e)

def getEmployees():
    query = "SELECT * FROM employees;"
    cur.execute(query)
    print("Empleados registrados:", cur.fetchall())

getEmployees()

def getDepartments():
    query = "SELECT * FROM departments;"
    cur.execute(query)
    print("Departamentos registrados:", cur.fetchall())

getDepartments()



