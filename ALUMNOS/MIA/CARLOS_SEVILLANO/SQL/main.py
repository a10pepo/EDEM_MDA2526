import os, psycopg

try:
    #URL CONEXIÓN A BD 
    url = os.getenv("DATABASE_URL")
    #CONEXIÓN A BD
    connection = psycopg.connect(url)
    # Cursor
    cur = connection.cursor()
    print("BD conectada con éxito")

    # def getDepartments():
    #     query = "SELECT * FROM departments;"
    #     cur.execute(query)
    #     print("Nuestros departamentos:",cur.fetchall())
        
    # getDepartments()
    # def getEmployees():
    #     query = "SELECT * FROM employees;"
    #     cur.execute(query)
    #     print("Nuestros empleados:",cur.fetchall())
    
    # getEmployees()
    # def createDepartment(name):
    #      try:
    #           query = f"""INSERT INTO departments (name) VALUES ('{name}');"""
    #           cur.execute(query)
    #           print("Departamento creado")
    #      except:
    #           print('Error creando usuario')

    # createDepartment("Sustainability")
    # connection.commit()
    # def getEmployeesWithDepartments():
    #     query = """SELECT e.*,d.name FROM employees as e INNER JOIN departments as d ON
    #     e.department_id=d.id;"""
    #     cur.execute(query)
    #     print("Nuestros departamentos:",cur.fetchall())
        
    # getEmployeesWithDepartments()
    def createEmployee(birth_date,first_name,last_name,salary,title,title_date):
         try:
              query = f"""INSERT INTO employees (birth_date,first_name,last_name,salary,title,title_date) VALUES ('{birth_date}','{first_name}','{last_name}',{salary},'{title}','{title_date}');"""
              cur.execute(query)
              print("Departamento creado")
         except:
              print('Error creando departamento')

    createEmployee("2000-08-15","Jorge","Martinez Martinez",40000,"Informacion y Computacion", "2023-10-10")
    connection.commit()

except:
    print("Error conectando a la BD")
