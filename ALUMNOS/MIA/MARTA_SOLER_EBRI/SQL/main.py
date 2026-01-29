import os, psycopg
from datetime import date

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")

def getDepartments():
  query = "SELECT * FROM departments;"
  cur.execute(query)
  print("Nuestros departamentos:",cur.fetchall())
getDepartments()

def getEmployees():
  query = "SELECT * FROM employees;"
  cur.execute(query)
  print("Nuestros empleados:",cur.fetchall())
getEmployees()

def getEmployeesDepartments():
  query = """
    SELECT * FROM employees 
    INNER JOIN departments 
    ON employees.department_id=departments.id;
    """
  cur.execute(query)
  print("Nuestros empleados y sus departamentos:",cur.fetchall())
getEmployeesDepartments()

def createDepartment(name):
  try:
    query = "INSERT INTO departments (name) VALUES (%s)"
    cur.execute(query, (name,))
    connection.commit()
    print("Departamento creado.")
  except Exception as e:
    print("Error creando departamento:", e)
createDepartment("Audit")
connection.commit()

def createEmployee(birth_date, first_name, last_name, department_id):
  try:
    query = """
        INSERT INTO employees (birth_date, first_name, last_name, department_id) 
        VALUES (%s, %s, %s, %s)
        """
    cur.execute(query, (birth_date, first_name, last_name, department_id))
    connection.commit()
    print("Empleado creado.")
  except Exception as e:
    print("Error creando empleado:", e)
createEmployee("2002-10-24", "Marta", "Soler", "1")
connection.commit()
getEmployeesDepartments()

employees_data = [{"first_name": "Juan", "last_name": "Pérez", "department_id": 1, "birth_date": date(1990, 5, 15)},
                  {"first_name": "Ana", "last_name": "Gómez", "department_id": 2, "birth_date": date(1985, 11, 20)},
                  {"first_name": "Carlos", "last_name": "López", "department_id": 3, "birth_date": date(1995, 2, 28)}]

def createMultipleEmployees(employees_list):
    query = """
        INSERT INTO employees (
            first_name, last_name, department_id, birth_date
        ) VALUES (%s, %s, %s, %s)
    """
    try:
        print("Insertando múltiples empleados...")
        for employee in employees_list:
            values = (
                employee["first_name"],
                employee["last_name"],
                employee["department_id"],
                employee["birth_date"]
            )
            cur.execute(query, values)
            print(f"Insertado: {employee['first_name']} {employee['last_name']}")
        connection.commit()
        print("Todos los empleados han sido creados.")       
    except Exception as e:
        connection.rollback()
        print("Error creando empleados:", e)
createMultipleEmployees(employees_data)
getEmployeesDepartments()

cur.close()
connection.close()
print("Conexión a BD cerrada.")