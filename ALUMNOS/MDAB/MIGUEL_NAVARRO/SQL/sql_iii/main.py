import os, psycopg

# URL CONEXIÓN A BD
url = os.getenv("DATABASE_URL")
# CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")


# createTableDepartments()
# Debe crear la tabla departments
def createTableDepartments():
    try:
        query = """CREATE TABLE IF NOT EXISTS departments(
        id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        name        VARCHAR
        );"""
        cur.execute(query)
        connection.commit()
        print("departments table created (if not exists)")
    except Exception as e:
        print('Error creating departments table', e)

# createDepartment(name)
# Debe insertar un nuevo departamento con los datos que reciba por parámetro.
def createDepartment(name):
    try:
        query = "INSERT INTO departments (name) VALUES (%s);"
        cur.execute(query, (name,))
        connection.commit()
        print(f"department created: ", name)
    except Exception as e:
        print("Error creating department:", e)

# getDepartments()
# Debe mostrar todos los departamentos registrados.
def getDepartments():
    query = "SELECT * FROM departments;"
    cur.execute(query)
    print("Our departments:", cur.fetchall())

    
# EXTRA Practice

# createEmployee(first_name, last_name, email, department_id)
# Debe insertar un nuevo empleado, asignándolo automáticamente al departamento que le pases por id.
def createTableEmployees():
    try:
        query = """CREATE TABLE IF NOT EXISTS employees (
        id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        first_name      VARCHAR(100) NOT NULL,
        last_name       VARCHAR(100) NOT NULL,
        email           VARCHAR(100) NOT NULL,
        department_id   BIGINT NOT NULL REFERENCES departments(id)
        );"""
        cur.execute(query)
        connection.commit()
        print("employees table created")
    except Exception as e:
        print("Error creating employees table:", e)

def createEmployee(first_name, last_name, email, department_id):
    try:
        query = """INSERT INTO employees(first_name, last_name, email, department_id)
        VALUES(%s, %s, %s, %s);"""
        cur.execute(query, (first_name, last_name, email, department_id))
        connection.commit()
        print("employee created: ", first_name, last_name, email)
    except Exception as e:
        print("Error creating employee:", e)


# getEmployees()
# Debe mostrar todos los empleados.
def getEmployees():
    query = "SELECT * FROM employees;"
    cur.execute(query)
    print("Our employees:", cur.fetchall())

# getEmployeesWithDeparments()
# Debe mostrar todos los empleados junto con el nombre del departamento al que pertenecen.
def getEmployeesWithDepartments():
    query = """SELECT e.first_name, e.last_name, e.email, d.name
    FROM employees AS e
    LEFT JOIN departments AS d
    ON e.department_id = d.id;"""
    cur.execute(query)
    print("Our employees:", cur.fetchall())
    

# EXTRA:
# Crea una lista llamada employees que contenga varios diccionarios.
# Cada diccionario representará un empleado con su nombre, apellido, email y el ID del departamento al que pertenece (department_id).
# A continuación, recorre la lista con un bucle e inserta cada empleado en la tabla employees de forma automática utilizando una consulta parametrizada (%s).
# Recuerda confirmar los cambios con connection.commit() al finalizar.

employees = [
    {"first_name": "Miguel",    #1
     "last_name": "Herrera",
     "email": "miki@example.es",
     "department_id": 1},
    {"first_name": "Miguel",    #2
     "last_name": "Navarro",
     "email": "migue@example.es",
     "department_id": 2},
    {"first_name": "Andrea",    #3
     "last_name": "Granados",
     "email": "andy@example.es",
     "department_id": 2},
    {"first_name": "Javier",    #4
    "last_name": "Santos",
    "email": "javier.santos@example.com",
    "department_id": 3},
    {"first_name": "Laura",     #5
     "last_name": "Méndez",
     "email": "laura.mendez@example.net",
     "department_id": 1},
    {"first_name": "Carlos",    #6
    "last_name": "Ríos",
    "email": "carlos.rios@example.org",
    "department_id": 2},
    {"first_name": "Sofía",     #7
    "last_name": "Vargas",
    "email": "sofia.vargas@example.es",
    "department_id": 4}
]

createTableDepartments()
createDepartment("Human Resources")         #1
createDepartment("Data Analytics")          #2
createDepartment("Software Development")    #3
createDepartment("Digital Marketing")       #4

createTableEmployees()

n=0
while n<len(employees):
    createEmployee(employees[n]["first_name"], employees[n]["last_name"], employees[n]["email"], employees[n]["department_id"])
    n+=1

getEmployeesWithDepartments()