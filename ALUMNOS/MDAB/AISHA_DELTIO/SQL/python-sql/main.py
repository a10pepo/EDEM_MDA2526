import os, psycopg

# Importa la biblioteca os (Operating System). 
# Esta biblioteca estándar de Python te permite interactuar con el sistema operativo, 
# y su función más común es leer "variables de entorno".

# Importa la biblioteca os (psycopg). 
# Esta es la herramienta (el "driver") que sabe cómo "hablar" el protocolo de PostgreSQL.



# URL CONEXIÓN A BD 
# Le pide al sistema operativo "dame el valor de la variable de entorno que se llama DATABASE_URL".
url = os.getenv("DATABASE_URL")

#CONEXIÓN A BD
connection = psycopg.connect(url)

# CURSOR
# Crea un objeto "cursor".
# No puedes enviar comandos SQL directamente con la connection. Necesitas un cursor, que es como el "controlador" que ejecuta tus comandos y te devuelve los resultados.
# A partir de aquí, para hacer cualquier cosa en la base de datos, usarías este objeto cur.

cur = connection.cursor()

print("BD conectada con éxito")

# createTableUsers(). Debe crear la tabla departments
def createTableUsers():
    try:
        query = """CREATE TABLE users (
                        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL
                        );"""
        cur.execute(query)
        print("Tabla creada")
    except:
        print('Error creando tabla')
# createTableUsers()

# getUsers
def getUsers():
    query = "SELECT * FROM users;"
    cur.execute(query)
    print("Nuestros usuarios:",cur.fetchall())

getUsers()


# createUser
def createUser():
    try:
        query = """INSERT INTO users (first_name, last_name, email, password) 
        VALUES ('Miguel','Herrera','miki@example.com','123456');"""
        cur.execute(query)
        print("Usuario creado")
    except:
        print('Error creando usuario')
        
# createUser()
# connection.commit()

def createUser(first_name, last_name, email, password):
    try:
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (first_name, last_name, email, password))
        connection.commit()
        print("Usuario creado")
    except Exception as e:
        print("Error creando usuario:", e)
        
# createUser("AISHA","DEL TIO","AAAA@gmail.com","fregtr344")
# connection.commit()


# EJERCICIOS PRACTICA PROFESORA SOFIA:

# createTableDepartments(). Debe crear la tabla departments
def createTableDepartments():
    try:
        query = """CREATE TABLE departments (
                        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        name TEXT NOT NULL
                        );"""
        cur.execute(query)
        print("Tabla creada")
    except:
        print('Error creando tabla')

# createTableDepartments()
# connection.commit()

# createDepartment(name). Debe insertar un nuevo departamento con los datos que reciba por parámetro.
def createDepartment(name):
    try:
        query = "INSERT INTO departments (name) VALUES (%s)"
        cur.execute(query, (name,))
        connection.commit()
        print("Departamento creado")
    except Exception as e:
        print("Error creando departamento:", e)
        
# createDepartment("Engineering")

# sin querer he añadido dos departamentos con el mismo nombre, para arreglarlo:

# (Asumo que 'cur' y 'connection' ya están definidos y conectados)

def updateDepartmentName(department_id, new_name):
    try:
        query = "UPDATE departments SET name = %s WHERE id = %s"
        cur.execute(query, (new_name, department_id))
        connection.commit() 
        print(f"Departamento ID {department_id} actualizado a '{new_name}' con éxito.")
        
    except Exception as e:
        print(f"Error actualizando departamento {department_id}:", e)

# updateDepartmentName(2, "Marketing")


# getDepartments(). Debe mostrar todos los departamentos registrados
def getDepartments():
    query = "SELECT * FROM departments;"
    cur.execute(query)
    print("Nuestros departamentos:",cur.fetchall())

# getDepartments()


# EJERCICIOS EXTRA PROFESORA SOFIA:

# createEmployee(first_name, last_name, email, department_id). Debe insertar un nuevo empleado, asignándolo automáticamente al departamento que le pases por id.

# creamos la tabla para empleados con la FK
def createTableEmployee():
    try:
        query = """CREATE TABLE IF NOT EXISTS employees (
                        id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        birth_date  DATE NOT NULL,  
                        first_name  VARCHAR(100) NOT NULL,
                        last_name   VARCHAR(255) NOT NULL,
                        department_id INTEGER REFERENCES departments(id)
                    );"""
        cur.execute(query)
        print("Tabla createTableEmployee creada")
    except Exception as e:
        print('Error creando tabla: createTableEmployee', e)

# createTableEmployee()
# connection.commit()

# como no hemos creado la tabla con las columnas que queremos, lo modificamos:
def modTableEmployee():
    try:
        query = """ALTER TABLE employees
                    ADD COLUMN email VARCHAR(255) UNIQUE NOT NULL,
                    ADD COLUMN title VARCHAR(100),
                    DROP COLUMN birth_date;"""
        cur.execute(query)
        print("mod")
    except Exception as e:
        print('no mod', e)
        
# modTableEmployee()
# connection.commit()

# ahora quiero ver como me ha quedado finalmente la tabla de employees
def vertable(table_name):
    try:
        query = """
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = %s;
        """
        cur.execute(query, (table_name,))
        columns = cur.fetchall()
        
        if columns:
            print(f"--- Estructura de la tabla: {table_name} ---")
            for col in columns:
                print(f"  Columna: {col[0]}, Tipo: {col[1]}")
            print("----------------------------------------")
        else:
            print(f"La tabla '{table_name}' no existe o está vacía.")
            
    except Exception as e:
        print(f"Error al ver la tabla '{table_name}':", e)

# vertable("employees")
# vertable("departments")


# añadimos employees junto a departamentos
def createEmployee(first_name, last_name, email, title, department_id):
    try:
        query = """
        INSERT INTO employees (first_name, last_name, email, title, department_id) 
        VALUES (%s,%s,%s,%s,%s)
        """
        params = (first_name, last_name, email, title, department_id)
        cur.execute(query, params)
        print("Empleado añadido")
    except Exception as e:
        print("Error creando empleado:", e)
        
# createEmployee("Aisha","del Tio","adetpp@gmail.com","Ingeniera Junior",1)
# connection.commit()

# getEmployees(). Debe mostrar todos los empleados.
def getEmployees():
    query = """
            SELECT id, first_name, last_name, email, title, department_id 
            FROM employees; 
            """
    cur.execute(query)
    print("Nuestros employees:",cur.fetchall())
    
# getEmployees()


# getEmployeesWithDeparments(). Debe mostrar todos los empleados junto con el nombre del departamento al que pertenecen.
def getEmployeesWithDeparments():
    query = """
            SELECT 
                e.first_name, 
                e.last_name,  
                d.name AS department_name
            FROM 
                employees e
            JOIN departments d ON e.department_id = d.id 
            """
    cur.execute(query)
    print("Nuestros employees con el nombre del departamento al que pertenecen:",cur.fetchall())
    
# getEmployeesWithDeparments()


# Crea una lista llamada employees que contenga varios diccionarios.
# Cada diccionario representará un empleado con su nombre, apellido, email y el ID del departamento al que pertenece (department_id).
# A continuación, recorre la lista con un bucle e inserta cada empleado en la tabla employees de forma automática utilizando una consulta parametrizada (%s).
# Recuerda confirmar los cambios con connection.commit() al finalizar.

employees = [
    # Engineering (ID 1)
    {'nombre': 'Elena', 'apellido': 'Vega', 'email': 'elena.vega@ejemplo.com', 'department_id': 1},
    {'nombre': 'Marco', 'apellido': 'Silva', 'email': 'marco.silva@ejemplo.com', 'department_id': 1},
    {'nombre': 'Laura', 'apellido': 'Gimenez', 'email': 'laura.gimenez@ejemplo.com', 'department_id': 1},
    {'nombre': 'Javier', 'apellido': 'Muñoz', 'email': 'javier.munoz@ejemplo.com', 'department_id': 1},

    # Marketing (ID 2)
    {'nombre': 'Sofia', 'apellido': 'Reyes', 'email': 'sofia.reyes@ejemplo.com', 'department_id': 2},
    {'nombre': 'Daniel', 'apellido': 'Ortega', 'email': 'daniel.ortega@ejemplo.com', 'department_id': 2},
    {'nombre': 'Lucia', 'apellido': 'Campos', 'email': 'lucia.campos@ejemplo.com', 'department_id': 2},
    
    # Sin Departamento (None)
    {'nombre': 'Ana', 'apellido': 'Perez', 'email': 'ana.perez@ejemplo.com', 'department_id': None},
    {'nombre': 'David', 'apellido': 'Gomez', 'email': 'david.gomez@ejemplo.com', 'department_id': None},
]


def insertar_empleados_en_lote(lista_de_empleados):
    try:
        # 1. La consulta que usaremos en cada vuelta
        query = """
        INSERT INTO employees (first_name, last_name, email, department_id) 
        VALUES (%s, %s, %s, %s)
        """
        for empleado in lista_de_empleados:
            params = (
                empleado['nombre'], 
                empleado['apellido'], 
                empleado['email'], 
                empleado['department_id']
            )
            cur.execute(query, params)
        connection.commit()
        print("¡Éxito! Todos los empleados fueron guardados.")

    except Exception as e:
        print(f"ERROR: {e}")
      
# insertar_empleados_en_lote(employees)
# getEmployeesWithDeparments()