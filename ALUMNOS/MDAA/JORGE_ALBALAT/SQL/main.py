def getDepartments(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Departments;")
    
    # fetchall() recupera todas las filas del resultado de la consulta
    return cursor.fetchall()

def getEmployees(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employees;")
    return cursor.fetchall()

def getEmployeesWithDepartments(conn):
    cursor = conn.cursor()
    
    # Usamos un INNER JOIN para combinar las tablas
    query = """
        SELECT 
            Employees.EmployeeID,
            Employees.EmployeeName, 
            Departments.DepartmentName
        FROM 
            Employees
        INNER JOIN 
            Departments ON Employees.DepartmentID = Departments.DepartmentID;
    """
    cursor.execute(query)
    return cursor.fetchall()