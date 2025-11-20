import os, psycopg
#URL CONEXIÓN A BD
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")


# getUsers
# Esta función lee e imprime todos los usuarios de la tabla usersde tu base de datos PostgreSQL.
# SELECT * FROM users; : obtiene todos los datos.
# cur.fetchall() : los recoge.
# print() : los muestra por consola.

