import os, psycopg

url = os.getenv("DATABASE_URL")
connection = psycopg.connect(url)
cur = connection.cursor()
print("BD conectada con éxito")

# Práctica (Diapo. 27)

# Crea las siguientes funciones en tu main.py:

# getDepartments(). Debe mostrar todos los departamentos registrados.

def getDepartments():
    query = "SELECT * FROM departments;"
    cur.execute(query)
    print("Nuestros departamentos:",cur.fetchall())
getDepartments()

# getEmployees(). Debe mostrar todos los empleados.

def getEmployees():
    query = "SELECT * FROM employees;"
    cur.execute(query)
    print("Nuestros empleados:",cur.fetchall())
getEmployees()

# getEmployeesWithDeparments(). Debe mostrar todos los empleados junto con el nombre del departamento al que pertenecen.

def getEmployeesWithDeparments():
    query = """SELECT employees.first_name, employees.last_name, departments.departments_name 
            FROM employees 
            JOIN departments ON employees.departments_id = departments.departments_id;"""
    cur.execute(query)
    print("Empleados con sus departamentos:",cur.fetchall())
getEmployeesWithDeparments()

# Extra (Diapo. 28)

# Crea las siguientes funciones en tu main.py:

# createDepartment(name). Debe insertar un nuevo departamento con los datos que reciba por parámetro.

def createDepartment(departments_name):
    try:
        query = "INSERT INTO departments(departments_name) VALUES (%s)"
        cur.execute(query, (departments_name,))
        connection.commit()
        print("Departamento creado")
    except Exception as e:
        print("Error creando departamento:", e)

createDepartment("Science")
connection.commit()

# createEmployee(first_name, last_name, email, department_id). Debe insertar un nuevo empleado, asignándolo automáticamente al 
# departamento que le pases por id.

# Le tengo que poner birth_date sí o sí porque en la tabla no puede ser nunca NULL. 

def ensureEmailColumnExists():
    try:
        query_check = """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='employees' AND column_name='email';
        """
        cur.execute(query_check)
        result = cur.fetchone()

        if not result:
            print("La columna 'email' no existe. Creándola...")
            cur.execute("ALTER TABLE employees ADD COLUMN email VARCHAR(100);")
            connection.commit()
            print("Columna 'email' creada correctamente.")
    except Exception as e:
        print("Error comprobando o creando la columna email:", e)


def createEmployee(first_name, last_name, email, departments_id, birth_date):
    try:
        ensureEmailColumnExists()

        query = """
            INSERT INTO employees (first_name, last_name, email, departments_id, birth_date)
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(query, (first_name, last_name, email, departments_id, birth_date))
        connection.commit()
        print("Empleado creado correctamente.")
    except Exception as e:
        print("Error creando empleado:", e)

createEmployee("Celia", "Sarrió", "celiasarrio34@gmail.com", 4, "1990-12-14")
connection.commit()

# Extra (Diapo. 29)

# Crea una lista llamada employees que contenga varios diccionarios.
# Cada diccionario representará un empleado con su nombre, apellido, email y el ID del departamento al que pertenece (department_id).
# A continuación, recorre la lista con un bucle e inserta cada empleado en la tabla employees de forma automática utilizando una consulta parametrizada (%s).
# Recuerda confirmar los cambios con connection.commit() al finalizar.

employees = [
    {"first_name": "Ana", "last_name": "García", "email": "anagarcia@example.com", "departments_id": 1, "birth_date": "1990-08-22"},
    {"first_name": "Luis", "last_name": "Martínez", "email": "luismartinez@example.com", "departments_id": 2, "birth_date": "1970-11-17"},
    {"first_name": "Marta", "last_name": "López", "email": "martalopez@example.com", "departments_id": 1, "birth_date": "1998-09-02"},
    {"first_name": "Carlos", "last_name": "Sánchez", "email": "carlossanchez@example.com", "departments_id": 3, "birth_date": "1940-02-10"}
]

for emp in employees:
    createEmployee(emp["first_name"], emp["last_name"], emp["email"], emp["departments_id"], emp["birth_date"])    
connection.commit()