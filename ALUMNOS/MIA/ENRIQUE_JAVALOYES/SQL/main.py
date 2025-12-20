import os, psycopg

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")

#CONEXIÓN A BD​
connection = psycopg.connect(url)

# Cursor​
cur = connection.cursor()

print("BD conectada con éxito")


def getDepartments():

    query = "SELECT * FROM departments;"

    cur.execute(query)

    print("Nuestros departamentos:",cur.fetchall())

getDepartments()


def getEmployees():

    query = "SELECT * FROM employees;"

    cur.execute(query)

    print("Nuestros empleados:",cur.fetchall())

getEmployees()


def getEmployeesWithDeparments():

    query = "SELECT e.first_name, e.last_name, e.salary,d.nombre AS nombre_departamento FROM employees e LEFT JOIN departments d ON e.department_id = d.id;"
    cur.execute(query)

    print("Nuestros empleados y sus departamentos:",cur.fetchall())

getEmployeesWithDeparments()