import os, psycopg

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
try:
    cur = connection.cursor()
    print("BD conectada con éxito")
except psycopg.Error as e:
    print("Error conectando a la BD:", e)


def getemployees(cur):
    query = "SELECT * FROM employees;"
    cur.execute(query)
    print("Nuestros empleados:",cur.fetchall())

getemployees(cur)


def getdepartments(cur):
    query = "SELECT * FROM departments;"
    cur.execute(query)
    print("Nuestros deartamentos:",cur.fetchall())

getdepartments(cur)

def getEmployeesWithDepartments(cur):
    query = "SELECT * FROM employees INNER JOIN departments ON departments.id = employees.departments_id;"
    cur.execute(query)
    print("Estos son los empleados que tienen un departamento:", cur.fetchall())


getEmployeesWithDepartments(cur)





