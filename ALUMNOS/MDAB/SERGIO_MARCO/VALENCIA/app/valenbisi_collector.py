import os, time
from funciones import f_conexion_bd, f_run_ingestion


API_URL = "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records?limit=20"
DATABASE_URL = os.getenv("DATABASE_URL")


#CONEXIÓN A BD con intentos y tiempo de espera

connection = f_conexion_bd(DATABASE_URL,"valenbisi_db")

# Cursor.
# Crea un cursor, que es un objeto que permite ejecutar comandos SQL.
# - El cursor es como un "canal" entre tu código y la base de datos: puedes enviar consultas (SELECT, INSERT, etc.) y recibir resultados.
cur = connection.cursor()
print("Cursor creado con éxito")

#=============================================#
#=========== CREACIÓN TABLA ==================#
#=============================================#

cur.execute("""
                CREATE TABLE IF NOT EXISTS valenbisi_raw (
                    id SERIAL PRIMARY KEY,
                    station_id INTEGER NOT NULL,
                    station_name VARCHAR(255),
                    latitude DECIMAL(10, 8),
                    longitude DECIMAL(11, 8),
                    available_bikes INTEGER,
                    available_slots INTEGER,
                    station_status VARCHAR(50),
                    total_capacity INTEGER,
                    timestamp TIMESTAMP NOT NULL
                );
        """)

connection.commit()
cur.close()
connection.close()

if __name__ == "__main__":
    while True:
        try:
            f_run_ingestion(DATABASE_URL, API_URL)
        except Exception as e:
            print(f"Error en la captura: {e}")
        
        print("Esperando 5 minutos para la siguiente consulta...")
        time.sleep(300)

