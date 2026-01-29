import os, psycopg

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")


# def getEmployees():
    query = "SELECT * FROM employees;"
    cur.execute(query)
    print("Nuestros empleados:",cur.fetchall())
getEmployees()

def getDepartments():
    query = "SELECT * FROM departments;"
    cur.execute(query)
    print("Nuestros departamentos:",cur.fetchall())  
getDepartments()

def getEmployeesWithDepartments():
    query = "SELECT e.first_name, e.last_name, d.name FROM employees AS e INNER JOIN departments AS d ON e.department_id = d.id"
    cur.execute(query)
    print("Estos son los empleados que tienen un depertamento:",cur.fetchall())
    
getEmployeesWithDepartments()