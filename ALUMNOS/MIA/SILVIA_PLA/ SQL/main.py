import os, psycopg

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")


def createTableDepartments():
    query = """CREATE TABLE IF NOT EXISTS departments (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);"""
    cur.execute(query)

createTableDepartments()

def createTableEmployees():
    query = """CREATE TABLE employees(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(255)  NOT NULL
    );"""
    cur.execute(query)

createTableEmployees()

def getDepartments():
    query = "SELECT * FROM departments;"
    cur.execute(query)
    print("Nuestros usuarios:",cur.fetchall())

getDepartments()


def getEmployees():
    query = "SELECT * FROM employees;"
    cur.execute(query)
    print("Nuestros usuarios:",cur.fetchall())

getEmployees()
