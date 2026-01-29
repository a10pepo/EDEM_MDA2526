import os, psycopg

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
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

def getEmployeesWithDepartment():
    query = """
    SELECT employees.id, employees.name, departments.name 
    FROM employees
    JOIN departments ON employees.department_id = departments.id;
    """
    cur.execute(query)
    print("Empleados con sus departamentos:",cur.fetchall())