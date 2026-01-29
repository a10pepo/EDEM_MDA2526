import os, psycopg

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")


def getDepartments ():
    query = "SELECT departments.name FROM departments"
    cur.execute(query)
    print("Departamentos:",cur.fetchall())

getDepartments()


def getEmployees ():
    query = "SELECT employees.first_name FROM employees"
    cur.execute(query)
    print("Empleados:",cur.fetchall())

getEmployees()


def getEmployeesWithDeparments():
    query = "SELECT employees.first_name, departments.name FROM employees INNER JOIN departments ON employees.department_id= departments.department_id"
    cur.execute(query)
    print(cur.fetchall())

getEmployeesWithDeparments()

def createDepartment():
    try:
        query = "INSERT INTO departments (name) VALUES ('Informatica')"
        cur.execute(query)
        connection.commit()
        print("Departamento creado")
    except Exception as e:
        print("Error creando departamento:", e)

createDepartment()
connection.commit()
