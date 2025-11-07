import os, psycopg

url = os.getenv("DATABASE_URL")

connection = psycopg.connect(url)

cur = connection.cursor()

print("BD conectada con exito")



def getUsers():
    query = "SELECT * FROM employees;"
    cur.execute(query)
    print("Nuestros usuarios:", cur.fetchall())
    
getUsers()

def createUsers():
    try:
        query = """INSERT INTO employees (first_name, last_name, email, password)
        VALUES ('Miguel', 'Herrera', 'miki@example.com', '12324');"""
        cur.execute(query)
        print("Usuario creado")
    except:
        print("Error creando usuario")

connection.commit()


def createUsers(first_name, last_name, email,password):
    try:
        query = "INSERT INTO employees(first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
        cur.execute(query,(first_name, last_name, email, password))
        connection.commit()
        print("Usuario creado")
    except Exception as e:
        print("Error creando usuario")
        
createUsers("Federico", "Garcia", "fede@example.com", "1234555")


def createUser(birth_date, first_name, last_name, salary):
    try:
        query = "INSERT INTO employees (birth_date, first_name, last_name, salary) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (birth_date, first_name, last_name, salary))
        connection.commit()
        print("Usuario creado")
    except Exception as e:
        print("Error creando usuario:", e)

createUser("2021-05-22","Eusebio","García",50000.00)


def getDepartments():
    try:
        query = "SELECT nombre FROM departments;"
        cur.execute(query)
        connection.commit()
        print("Estos son los departamentos", cur.fetchall())
    except:
        print("No se han podido obtener los depts")
        
    
getDepartments()

def getEmployees():
    try:
        query = "SELECT first_name FROM employees;"
        cur.execute(query)
        connection.commit()
        print("Estos son los trabajadores: ", cur.fetchall())
    except:
        print("Error mostrando empleados")

getEmployees()

def getEmployeesDepts():
    query = """SELECT first_name, nombre 
    FROM employees
    INNER JOIN departments 
    ON departments.id = employees.department_id"""
    cur.execute(query)
    connection.commit()
    print("Estos son los empleados y sus depts: ", cur.fetchall())

getEmployeesDepts()

