import os, psycopg

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
# print("BD conectada con éxito")

def getDepartments():
    query = "SELECT * FROM departments;"
    cur.execute(query)
    print("Nuestros Departamentos:", cur.fetchall())

getDepartments()

def getEmployees():
    query ="SELECT * FROM employees;"
    cur.execute(query)
    print("Nuestros empleados", cur.fetchall())

getEmployees()

def getEmployeesWithDepartments():
    query = "SELECT * FROM employees INNER JOIN departments ON departments.id = employees.departments_id;"
    cur.execute(query)
    print("Estos son los empleados que tienen un departamento:", cur.fetchall())
    

getEmployeesWithDepartments()
