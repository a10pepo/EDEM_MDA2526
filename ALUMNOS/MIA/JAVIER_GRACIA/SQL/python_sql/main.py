import os, psycopg

print("Conectando a la BD...")
#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")

def _print_query_results(rows):
    if not rows:
        print("No hay registros.")
        return
    try:
        cols = [d.name for d in cur.description]
    except Exception:
        cols = [d[0] for d in cur.description]
    print(" | ".join(cols))
    for r in rows:
        print(r)


def getDepartments():
    """Muestra todos los departamentos registrados."""
    cur.execute("SELECT * FROM departments ORDER BY id;")
    rows = cur.fetchall()
    if not rows:
        print("No hay departamentos registrados.")
        return
    print("Departamentos:")
    _print_query_results(rows)


def getEmployees():
    """Muestra todos los empleados."""
    cur.execute("SELECT * FROM employees ORDER BY id;")
    rows = cur.fetchall()
    if not rows:
        print("No hay empleados registrados.")
        return
    print("Empleados:")
    _print_query_results(rows)


def getEmployeesWithDeparments():
    """Muestra todos los empleados junto con el nombre del departamento."""
    cur.execute(
        """
        SELECT e.*, d.name AS department_name
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        ORDER BY e.id;
        """
    )
    rows = cur.fetchall()
    if not rows:
        print("No hay empleados o departamentos relacionados.")
        return
    print("Empleados con departamento:")
    _print_query_results(rows)

def createDepartment(name):
    """Inserta un nuevo departamento con el nombre dado y devuelve su id."""
    try:
        cur.execute(
            "INSERT INTO departments (name) VALUES (%s) RETURNING id;",
            (name,)
        )
        new_id = cur.fetchone()[0]
        connection.commit()
        print(f"Departamento creado con id {new_id}.")
        return new_id
    except Exception as e:
        connection.rollback()
        print("Error creando departamento:", e)
        return None

def createEmployee(first_name, last_name, department_id, birth_date):
    """Inserta un nuevo empleado y lo asigna al departamento indicado por id."""
    try:
        # Comprobar que el departamento existe
        cur.execute("SELECT id FROM departments WHERE id = %s;", (department_id,))
        if cur.fetchone() is None:
            print("Departamento no encontrado. No se creó el empleado.")
            return None
        cur.execute(
            """
            INSERT INTO employees (first_name, last_name, department_id, birth_date)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
            """,
            (first_name, last_name, department_id, birth_date)
        )
        new_id = cur.fetchone()[0]
        connection.commit()
        print(f"Empleado creado con id {new_id}.")
        return new_id
    except Exception as e:
        connection.rollback()
        print("Error creando empleado:", e)
        return None

getDepartments()
print("\n")
getEmployees()
print("\n")
getEmployeesWithDeparments()

# Inserta empleados usando la función createEmployee definida arriba
employees = [
    {"first_name": "Ana", "last_name": "García", "birth_date": "1990-01-01", "department_id": 1},
    {"first_name": "Luis", "last_name": "Martínez", "birth_date": "1985-05-15", "department_id": 2},
    {"first_name": "María", "last_name": "López", "birth_date": "1992-08-30", "department_id": 1},
    {"first_name": "Jorge", "last_name": "Pérez", "birth_date": "1980-12-12", "department_id": 3},
    {"first_name": "Lucía", "last_name": "Fernández", "birth_date": "1995-03-22", "department_id": 2},
]

inserted = 0
for emp in employees:
    new_id = createEmployee(emp["first_name"], emp["last_name"], emp["department_id"], emp["birth_date"])
    if new_id is not None:
        inserted += 1

print(f"{inserted} empleados insertados correctamente.")

# Cerrar cursor y conexión
cur.close()
connection.close()
print("\nConexión cerrada.")

