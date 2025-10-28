import os, psycopg

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")

# def getdepartments():
#   query = "SELECT * FROM departments;"
#   cur.execute(query)
#   print("Departamentos registrados: ",cur.fetchall())

# getdepartments()



# def getemployees():
#   query = "SELECT * FROM employees;"
#   cur.execute(query)
#   print("Estos son los empleados: ",cur.fetchall())

# getemployees()



def getemployeesWithDepartments():
  query = "SELECT e.first_name, e.last_name, d.name FROM employees AS e INNER JOIN departments AS d ON e.departments_id = d.id"
  cur.execute(query)
  print("Estos son los empleados que tienen un departamento: ",cur.fetchall())

getemployeesWithDepartments()
