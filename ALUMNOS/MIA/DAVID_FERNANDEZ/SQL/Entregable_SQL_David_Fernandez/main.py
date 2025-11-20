import os, psycopg

url = os.getenv("DATABASE_URL")

connection = psycopg.connect(url)

cur = connection.cursor()
print("BD conectada con éxito")

def getdepartments():
    query = "SELECT * FROM departments;"
    cur.execute(query)
    print("Nuestros usuarios:",cur.fetchall())

getdepartments()

def createemployees():
    try:
        query = "SELECT * FROM employees;"
        cur.execute(query)
        print()
    except:
        print('Error creando usuario')

createemployees()
connection.commit()

def getEmployeesWithDeparments():
    try:
        query = """
        SELECT * FROM employees
        INNER JOIN departments ON employees.department_id = departments.id
        """
    except:
        print('Error creando usuario')
        