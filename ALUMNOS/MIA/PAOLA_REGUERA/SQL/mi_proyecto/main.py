import os, psycopg
# URL CONEXION A BD
url= os.getenv("DATABASE_URL")
# CONEXION A BD
connection= psycopg.connect(url)
# CURSOR
cur= connection.cursor()
print("BD conectada con éxito")


# def getDepartments():
#     query = "SELECT * FROM departments;"
#     cur.execute(query)
#     print("Nuestros departamentos:",cur.fetchall())
# getDepartments()

# def getEmployees():
#     query = "SELECT * FROM employees;"
#     cur.execute(query)
#     print("Nuestros trabajadores:",cur.fetchall())
# getEmployees()

def getEmployeesWithDepartments():
    query = """SELECT employees.id, employees.first_name, employees.last_name, departments.name
        FROM employees 
        JOIN departments ON employees.department_id = departments.id;"""
    cur.execute(query)
    print("Trabajadores con sus departamentos:",cur.fetchall())
getEmployeesWithDepartments()
