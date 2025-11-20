import os, psycopg

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")

def getDepartments():
    query = "SELECT name FROM departments;"
    cur.execute(query)
    print("Nuestros departamentos:",cur.fetchall())

getDepartments()

def getEmployees():
    query = "SELECT first_name || ' ' ||  last_name FROM employees;"
    cur.execute(query)
    print("Nuestros empleados:", cur.fetchall())

getEmployees()

def getEmployeesWithDepartments():
    query = """SELECT employees.first_name, departments.name
            FROM employees
            INNER JOIN departments
            ON employees.department_id = departments.id;"""
    cur.execute(query)
    print("Nuestros empleados y sus departamentos:",cur.fetchall())

getEmployeesWithDepartments()