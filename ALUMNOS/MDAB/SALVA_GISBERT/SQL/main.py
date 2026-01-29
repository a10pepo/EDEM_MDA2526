import os, psycopg
#URL CONEXIÓN A BD
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")

def createTableDepartments():
    try:
        query = """
        CREATE TABLE IF NOT EXISTS departments(
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name VARCHAR(100)
        )
        """
        cur.execute(query)
        connection.commit()
        print("Tabla creada")
    except Exception as e:
        print("Error creando tabla:", e)

def createDepartment(name):
    try:
        query = """
        INSERT INTO departments(name)
        VALUES(%s) 
        """ 
        cur.execute(query, (name,))
        connection.commit()
        print("Departamento añadido")

    except Exception as e:
        print("Error añadiendo departamento:", e)       

def getDepartments():
    try:
        query = """
        SELECT * 
        FROM departments
        """
        cur.execute(query)
        rows = cur.fetchall()
        print("Departamentos existentes:")
        for row in rows:
            print(row)
    except Exception as e:
        print("Error obteniendo departamentos:", e)  

def createTableEmployees():
    try:
        query = """
        CREATE TABLE IF NOT EXISTS employees(
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            email VARCHAR(100),
            department_id INT REFERENCES departments(id)
        )
        """
        cur.execute(query)
        connection.commit()
        print("Tabla employees creada")
    except Exception as e:
        print("Error creando tabla employees:", e)

def createEmployee(first_name, last_name, email, department_id):
    try:
        query = """
        INSERT INTO employees(first_name, last_name, email, department_id)
        VALUES(%s, %s, %s, %s)
        """
        cur.execute(query, (first_name, last_name, email, department_id))
        connection.commit()
        print("Empleado creado")

    except Exception as e:
        print("Error creando empleado:", e)  

def getEmployees():
    try:
        query = """
        SELECT * 
        FROM employees
        """
        cur.execute(query)
        rows = cur.fetchall()
        print("Empleados existentes:")
        for row in rows:
            print(row)
    except Exception as e:
        print("Error obteniendo departamentos:", e)  

def getEmployeesWithDepartments():
    try:
        query = """
        SELECT e.first_name, e.last_name, d.name 
        FROM employees AS e
        INNER JOIN departments AS d
        ON e.department_id = d.id
        """
        cur.execute(query)
        rows = cur.fetchall()
        print("Empleados con departamento:")
        for row in rows:
            print(row)
    except Exception as e:
        print("Error obteniendo empleados con departamento:", e)  

employees = [
    {"first_name": "Pablo", "last_name": "Fernández", "email": "pafer@pp.es", "department":1},
    {"first_name": "Rodrigo", "last_name": "Fernández", "email": "rofer@pp.es", "department":1},
    {"first_name": "Rocío", "last_name": "Martínez", "email": "pafer@pp.es", "department":1}
]

def addEmployees(employees):
    try:
        query = """
        INSERT INTO employees (first_name, last_name, email, department_id)
        VALUES (%s, %s, %s, %s)
        """
        data = [
            (emp["first_name"], emp["last_name"], emp["email"], emp["department"])
            for emp in employees
        ]
        cur.executemany(query, data)
        connection.commit()
        print(f"{len(employees)} empleados añadidos correctamente.")
    except Exception as e:
        print("Error añadiendo empleados:", e)
        connection.rollback()



createTableDepartments()
createDepartment("Engineering")
getDepartments()
createTableEmployees()
createEmployee("Lucas", "Gómez", "lugo@lll.com", 1)
getEmployees()
getEmployeesWithDepartments()
addEmployees(employees)
getEmployees()

connection.commit()