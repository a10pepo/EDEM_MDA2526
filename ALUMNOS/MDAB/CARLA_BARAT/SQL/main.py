import os, psycopg


# URL de conexión a la base de datos desde .env
url = os.getenv("DATABASE_URL")


    # Conectar a la base de datos
connection = psycopg.connect(url)
cur = connection.cursor()
print("BD conectada con éxito ")

    # Crear tabla si no existe
cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );
    """)
connection.commit()

    # Insertar algunos usuarios de ejemplo (solo si la tabla está vacía)
cur.execute("SELECT COUNT(*) FROM users;")
if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO users (name) VALUES ('Carla'), ('Lucía'), ('Marcos');")
        connection.commit()

    # Función para obtener usuarios
def getUsers():
        query = "SELECT * FROM users;"
        cur.execute(query)
        print("Nuestros usuarios:", cur.fetchall())

    # Llamar a la función
getUsers()
