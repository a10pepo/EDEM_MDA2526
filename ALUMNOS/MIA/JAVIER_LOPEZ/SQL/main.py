import os, psycopg

#URL CONEXIÓN A BD 

url = os.getenv("DATABASE_URL")

if not url:
    raise ValueError("No se encontró la variable DATABASE_URL en el entorno.")

# Intentar conexión
try:
    connection = psycopg.connect(url)
    cur = connection.cursor()
    print("BD conectada con éxito")
    
    def getEmployers():

        query = "SELECT * FROM employees;"

        cur.execute(query)
        print("Nuestros empleados:",cur.fetchall())

    def getDepartments():

        query = "SELECT * FROM departments;"

        cur.execute(query)
        print("Nuestros departamentos:",cur.fetchall())

    def getEmployeesWithDepartments():
        query = ("SELECT employees.id, employees.first_name AS empleado, departments.nombre AS departamento " 
        "FROM employees INNER JOIN departments ON employees.department_id = departments.id")

        cur.execute(query)
        print("Empleados y su departamento: ", cur.fetchall())


    def createDepartment(nombre):
        try:
            query = "INSERT INTO departments (nombre) VALUES (%s)"

            cur.execute(query, (nombre,))
            print("Departamento creado")


        except Exception as e:
            print("Error creando departamento", e)

    

    def createEmployer(birth_date, first_name, last_name, salary, title, title_date):

        try:
            query = "INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date) VALUES (%s,%s,%s,%s,%s,%s)"
            cur.execute(query, (birth_date, first_name, last_name, salary, title, title_date))
            print("Empleado creado")

        except Exception as e:
            print("Error al crear empleado",e)


    createEmployer(
    "1990-05-12",    # birth_date
    "Juan",          # first_name
    "Pérez",         # last_name
    3500,            # salary
    "Ingeniero",     # title
    "2025-10-23"     # title_date
)
    

    # Cerrar cursor y conexión
    cur.close()
    connection.close()

except Exception as e:
    print("Error conectando la DB:", e)