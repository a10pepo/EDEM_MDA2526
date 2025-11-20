import os, psycopg

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")


def createTableEmployees():
    try:
        query = """CREATE TABLE employees (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL
        );"""
        cur.execute(query)
        print("Tabla creada AAAAAAAAAAAAAAAAAAAAAA")
    except:
        print('La tabla ya existe XXXXXXXXXXXXXXXXXXXXXX')

def createTableDepartments():
    try:
        query = """CREATE TABLE departments (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name VARCHAR(50) NOT NULL
        );"""
        cur.execute(query)
        print("Tabla creada")
    except:
        print('La tabla ya existe')

def createEmployees():
    try:
        query = """INSERT INTO employees (first_name, last_name, email, password) 
        VALUES ('Ana','García', 'anagarcia@gmail.com', 'password1'),
               ('Luis','Martínez', 'luisillo@hotmail.com', 'password2'),
               ('María','López','mariquilla@kiki.com', 'passwd3');"""
        cur.execute(query)
        print("Empleados creados AAAAAAAAAAAAAAAAAAAAAAAA")
    except:
        print('Error creando empleados XXXXXXXXXXXXXXXXXXXXXXX')

def createDepartments():
    try:
        query = """INSERT INTO departments (name) 
        VALUES ('Recursos Humanos'),
               ('Desarrollo'),
               ('Marketing');"""
        cur.execute(query)
        print("Departamentos creados")
    except:
        print('Error creando departamentos')


# def createUser():
#         try:
#             query = """INSERT INTO users (first_name, last_name, email, password) 
#             VALUES ('Miguel','Herrera','miki@example.com','123456');"""
#             cur.execute(query)
#             print("Usuario creado")
#         except:
#             print('Error creando usuario')

# def getUsers():
#     query = "SELECT * FROM users;"
#     cur.execute(query)
#     print("Nuestros usuarios:",cur.fetchall())

def meterContraintEmployees():
    try:
        query = "ALTER TABLE employees ADD COLUMN department_id INTEGER REFERENCES departments(id);"
        cur.execute(query)
        print("Constraint añadida")
    except:
        print("La constraint ya existe")

def assignDepartmentsToEmployees():
    try:
        query = """UPDATE employees 
        SET department_id = CASE 
            WHEN first_name = 'Ana' THEN 1
            WHEN first_name = 'Luis' THEN 2
            WHEN first_name = 'María' THEN 3
            ELSE NULL
        END;"""
        cur.execute(query)
        print("Departamentos asignados")
    except:
        print("Error asignando departamentos")

def getDepartments():
    query = "SELECT * FROM departments;"
    cur.execute(query)
    print("Nuestros departamentos:",cur.fetchall())

def getEmployees():
    query = "SELECT * FROM employees;"
    cur.execute(query)
    print("Nuestros empleados:",cur.fetchall())

def getEmployeesWithDepartments():
    query = """SELECT employees.first_name, employees.last_name, departments.name 
    FROM employees
    LEFT JOIN departments ON employees.department_id = departments.id;"""
    cur.execute(query)
    print("Empleados con departamentos:",cur.fetchall())



getEmployeesWithDepartments()

connection.commit()


