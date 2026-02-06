import os
from sqlalchemy import create_engine

# 1. Configuración de la Base de Datos
# Sacamos los datos de las variables de entorno definidas en el docker-compose / .env
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

# Construimos la URL de conexión
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Creamos el motor. 
# pool_pre_ping=True ayuda a recuperar la conexión si se corta.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
