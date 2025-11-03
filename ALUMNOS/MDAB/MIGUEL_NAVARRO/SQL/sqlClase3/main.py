import os, psycopg

# URL CONEXIÓN A BD
url = os.getenv("DATABASE_URL")
# CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")


def createTableDepartments():
    try:
        query = """CREATE TABLE IF NOT EXISTS departments(
        )
        """
        cur.execute(query)
        print("Hecho...")
    except:
        print("Error...")

