import os, psycopg2, datetime

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
print(url)
#CONEXIÓN A BD
connection = psycopg2.connect(url)
cur = connection.cursor()

# Cursor
def getDepartments():
    print("\n\n\nDepartments\n\n\n")
    
    cur.execute("SELECT * from departments;")
    
    print(cur.fetchall())
    
def getEmployees():
    print("\n\n\nEmployees\n\n\n")
    
    cur.execute("SELECT * from employees;")
    print(cur.fetchall())

def getEmployeesWithDepartments():
    print("\n\n\nEmployees with departments\n\n\n")
    
    cur.execute(
        """SELECT *,departments.name  from employees
        LEFT JOIN departments on employees.department_id = departments.id;
        """)
    print(cur.fetchall())

def createDepartment(DepartmentName):
    print("\n\n\Department insertion\n\n\n")
    cur.execute("INSERT INTO departments (name) VALUES (%s);", (DepartmentName,))
    print(f"Department '{DepartmentName}' added successfully.")


def createEmployee(first_name, last_name, salary, department_id):
    print("\n\n\nEmployee insertion\n\n\n")
    query="INSERT INTO employee (first_name, last_name, salary, department_id, birth_date, title, title_date) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(query, (first_name, last_name, salary, department_id,datetime.now(),"NULL",datetime.now()))
    print(f"Employee added successfully.")


try:
    createEmployee("Laura", "García", 55000,2)
    connection.commit()
    getEmployeesWithDepartments()
    
    print("BD conectada con éxito")
except Exception:
    print("Error conectando a la BD")