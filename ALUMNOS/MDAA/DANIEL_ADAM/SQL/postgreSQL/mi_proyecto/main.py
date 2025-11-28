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


def getUsers():
 query = "SELECT * FROM users;"
 cur.execute(query)
 print("Nuestros usuarios:",cur.fetchall())


#getUsers()


def createUser():
  try:
    query = """INSERT INTO users (first_name, last_name, email, password) 
    VALUES ('Miguel','Herrera','miki@example.com','123456');"""
    cur.execute(query)
    print("Usuario creado")
  except:
    print('Error creando usuario')

#createUser()
#connection.commit() # Si no pones esto no se guarda en la base de datos el cambio

# Vamos a hacerlo ahora con una funcion reutilizable
def createUser(first_name, last_name, email, password):
  try:
    query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
    cur.execute(query, (first_name, last_name, email, password))
    connection.commit()
    print("Usuario creado")
  except Exception as e:
    print("Error creando usuario:", e) # La e es para que devuelva el error original de SQL

#createUser("Eusebio","García","fffeusebio@gmail.com","123456") #Como hemos definido los VALUES con %S podemos añadirlos al invocar a la funcion
#createUser("Eusebia","Garcíolo","fffeusllebio@gmail.com","123456")
#createUser("Carlota","Florolo","fffcalolalal@gmail.com","123456")
#connection.commit()


# Práctica

def getDepartments():
  try:
    query = """SELECT name FROM departments"""
    cur.execute(query)
    print("Departamentos: ", cur.fetchall())
  except:
    print('Error mostrando departamentos')

getDepartments()


def getEmployees():
  try:
    query = """SELECT first_name || ' ' || last_name FROM employees"""
    cur.execute(query)
    print("Empleados: ", cur.fetchall())
  except:
    print('Error mostrando empleados')

getEmployees()


def getEmployeesDepts():
  try:
    query = """SELECT employees.first_name || ' ' || employees.last_name, departments.name
     FROM employees
     INNER JOIN departments
     ON departments.id = employees.department_id"""
    cur.execute(query)
    print("Empleados y departamentos: ", cur.fetchall())
  except:
    print('Error mostrando empleados y departamentos')

getEmployeesDepts()

