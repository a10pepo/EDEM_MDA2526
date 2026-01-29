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

# getDepartments(). Debe mostrar todos los departamentos registrados.

def getDepartments():
     query = "SELECT * FROM departments;"
     cur.execute(query)
     print("Nuestros departamentos:",cur.fetchall())

getDepartments()

#getEmployees(). Debe mostrar todos los empleados.

def getEmployees():
     query = "SELECT * FROM employees;"
     cur.execute(query)
     print("Nuestros empleados:",cur.fetchall())

getEmployees()

# getEmployeesWithDeparments(). Debe mostrar todos los empleados junto con el nombre del departamento al que pertenecen

def getEmployeesWithDeparments():
     query = """SELECT 
     employees.first_name AS name, 
     departments.dep_name AS departamento 
     FROM employees
     LEFT JOIN departments
     ON departments.id = employees.departments_id;"""
     cur.execute(query)
     print("Nuestros empleados y dptos:",cur.fetchall())

getEmployeesWithDeparments()

# docker compose up