import psycopg

# Conexión directa
connection = psycopg.connect("postgresql://postgres:postgres@localhost:5433/pruebadb")

cur = connection.cursor()
print("BD conectada con éxito")


def getUsers():
    query = "SELECT * FROM users;"
    cur.execute(query)
    print("Nuestros usuarios:",cur.fetchall())



getUsers()

