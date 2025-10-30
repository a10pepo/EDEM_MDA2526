import os, psycopg

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")

def getdepartments():
    try:
        query = "SELECT * FROM departments ;"
        cur.execute(query)
        print(cur.fetchall())
    except:
        print("Hay error")
# getdepartments()
def getemployees():
    try:
        query = "SELECT * FROM employees ;"
        cur.execute(query)
        print(cur.fetchall())
    except:
        print("Hay error")
# getemployees()
def getemployeeswithdepartments():
    try:
        query = "SELECT employees.first_name, departments.first_name FROM employees INNER JOIN departments ON employees.department_id=departments.id; ;"
        cur.execute(query)
        print(cur.fetchall())
    except:
        print("Hay error")
# getemployeeswithdepartments()

def createdepartmentname():
    try:
        query = "INSERT INTO departments (first_name) VALUES ('BECARIO');"
        cur.execute(query)
        print("si q esta entrando")
    except:
        print("Hay error")
createdepartmentname()
connection.commit()