import os, psycopg

try:
    #URL CONEXIÓN A BD 
    url = os.getenv("DATABASE_URL")
    #CONEXIÓN A BD
    connection = psycopg.connect(url)
    # Cursor
    cur = connection.cursor()
    print("BD conectada con éxito")
except:
    print("Error conectando a la BD")


# Mostrar todos los empleados
def getEmployees():
    try:
        query = "SELECT * FROM employees;"
        cur.execute(query)
        print("Nuestros empleados:",cur.fetchall())
    except Exception as e:
        print("Error al mostrar empleados: ", e)

getEmployees()


# Mostrar todos los departamentos
def getDepartments():
    try:
        query = "SELECT * FROM departments;"
        cur.execute(query)
        print("Nuestros departamentos:",cur.fetchall())
    except Exception as e:
        print("Error al mostrar departamentos: ", e)
        

getDepartments()

# Mostrar los empleados con el departamento
def getEmployeesDept():
    try:
        query = """SELECT e.*, d.name_dep
        FROM employees e
        INNER JOIN departments d
        ON e.id_dep = d.id_dep;"""
        cur.execute(query)
        print("Nuestros empleados y departamentos:",cur.fetchall())
    except Exception as e:
        print("Error al mostrar empleados y departamentos: ", e)

getEmployeesDept()

# Insertar un nuevo departamento
def createDepartment(name):
    try:
        query = """INSERT INTO departments (name_dep) VALUES (%s)"""
        cur.execute(query, (name,))
        connection.commit()
        print("Departamento creado con éxito :)")
    except Exception as e:
        print("Error al insertar el departamento: ", e)
        
createDepartment("Commercial")

# Insertar un nuevo empleado al departamento que se le asigne
def createEmployee(first_name, last_name, department_id):
    try:
        query = """INSERT INTO employees (first_name, last_name, id_dep) VALUES (%s, %s, %s)"""
        cur.execute(query, (first_name, last_name, department_id))
        connection.commit()
        print("Empleado creado con éxito :)")
    except Exception as e:
        print("Error al insertar el empleado: ", e)
        
createEmployee("Manolo", "Piedras", 6)

# EXTRA II
lista_empleados = [
    {
        "first_name":"Pepo",
        "last_name":"Perez",
        "id_dep":5
    },
    {
        "first_name":"Pepita",
        "last_name":"Perezas",
        "id_dep":4
    }
]

for empleado in lista_empleados:
    createEmployee(empleado["first_name"], empleado["last_name"], empleado["id_dep"])
# commit de todos los inserts
connection.commit()

# Comprobar que se han insertado los empleados
getEmployees()





