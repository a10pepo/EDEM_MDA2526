import requests
import duckdb
import csv
import os

# ================================
# 1. Llamada a la API
# ================================
url = "https://valencia.opendatasoft.com/api/records/1.0/search/"
params = {
    "dataset": "valenbisi-disponibilitat-valenbisi-dsiponibilidad",
    "rows": 1000
}

response = requests.get(url, params=params)
data = response.json()

# Extraemos los registros
estaciones_raw = data.get("records", [])

# ================================
# 2. Procesar datos
# ================================
estaciones = []
for rec in estaciones_raw:
    fields = rec.get("fields", {})
    estacion = {
        "station_id": fields.get("number"),
        "station_name": fields.get("address"),
        "available_bikes": fields.get("available"),
        "available_bike_stands": fields.get("free"),
        "state_station": fields.get("open"),
        "total_capacity": fields.get("total"),
        "time": fields.get("update_jcd")
    }
    estaciones.append(estacion)

print(f"Total estaciones descargadas: {len(estaciones)}")

# ================================
# 3. Guardar CSV (para seeds dbt)
# ================================
# Crear carpeta seeds si no existe
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
seeds_dir = os.path.join(project_root, "seeds")
os.makedirs(seeds_dir, exist_ok=True)

csv_path = os.path.join(seeds_dir, "valenbisi.csv")

keys = [
    "station_id",
    "station_name",
    "available_bikes",
    "available_bike_stands",
    "state_station",
    "total_capacity",
    "time"
]

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerows(estaciones)

print(f"CSV guardado en: {csv_path}")

# ================================
# 4. Insertar en DuckDB
# ================================
db_path = os.path.join(project_root, "valenbisi.duckdb")
con = duckdb.connect(db_path)

# Crear tabla
con.execute("""
    CREATE TABLE IF NOT EXISTS valenbisi (
        station_id INTEGER,
        station_name VARCHAR,
        available_bikes INTEGER,
        available_bike_stands INTEGER,
        state_station BOOLEAN,
        total_capacity INTEGER,
        time TIMESTAMP
    );
""")

# Insertar datos desde CSV
con.execute(f"""
    INSERT INTO valenbisi
    SELECT * FROM read_csv_auto('{csv_path}', HEADER=TRUE);
""")

print("Datos insertados correctamente en DuckDB.")

con.close()
