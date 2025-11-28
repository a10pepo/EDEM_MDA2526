# **Mis Apuntes: Docker, Python y Postgres**
Estos son los pasos que seguí para montar un entorno de desarrollo completo usando Docker para la base de datos (Postgres) y para mi aplicación (Python), conectándolos y trabajando de forma interactiva desde VSCode.
## **1. El Entorno con Docker Compose**
Usé un solo archivo docker-compose.yml para definir y levantar todo mi entorno. Esto creó dos "servidores" (contenedores) que pueden hablar entre sí:

- Servicio db:

Imagen: postgres:17-alpine. Es mi servidor de base de datos.\
env\_file: .env: Le pasé mi archivo .env para que Postgres supiera cómo llamarse (POSTGRES\_DB=pruebadb) y qué contraseña usar.\
volumes: [postgresDB:/...]: La parte más importante. Vinculé un "volumen" de Docker a la carpeta de datos de Postgres. Esto hace que si apago o borro el contenedor, mis datos (tablas, usuarios) sigan guardados en el volumen postgresDB y no se pierdan.\
ports: ["5433:5432"]: Expuse el puerto interno 5432 de Postgres al puerto 5433 de mi máquina (mi "localhost"). Esto me permitió conectarme a la base de datos desde la extensión de VSCode como si estuviera instalada en mi PC.

- Servicio app:

Imagen: python:3.11. Es mi entorno de Python.\
working\_dir: /app: Le dije que trabajara dentro de la carpeta /app del contenedor.\
volumes: ["./:/app"]: Vinculé mi carpeta actual (con main.py y requirements.txt) a la carpeta /app del contenedor. Gracias a esto, cualquier cambio que guardo en main.py desde VSCode se refleja instantáneamente dentro del contenedor.\
depends\_on: [db]: Le dije a app que no arrancara hasta que el servicio db estuviera listo.
## **2. Mi Flujo de Trabajo (Cómo ejecuté el código)**
Al principio, app solo ejecutaba python main.py y se apagaba. Esto no era útil para desarrollar.

La solución fue cambiar el command en docker-compose.yml por:\
command: sh -c "pip install -r requirements.txt && tail -f /dev/null"\
\
Esto instala las librerías (psycopg) y luego usa tail -f /dev/null, un truco que deja el contenedor vivo y "esperando".

Para ejecutar mi código desde la terminal de VSCode:

- docker compose exec app python main.py

Este comando "se mete" en el contenedor app que ya está corriendo y ejecuta el script main.py.
## **3. La Conexión Python (psycopg)**
Para conectar Python con Postgres, usé la librería psycopg.

Luego obtuve las dos herramientas principales:\
\
connection = psycopg.connect(url)\
cur = connection.cursor()\
\
connection es la conexión en sí.\
cur (cursor) es el "obrero" que uso para enviar comandos (cur.execute()) y recoger resultados (cur.fetchall()).

## **4. Continuar trabajando**
Cuando acabamos de trabajar: docker compose stop

Para volver a trabajar: docker composer start



