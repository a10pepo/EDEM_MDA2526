import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# Credenciales de tu RDS
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

conexion_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

print("📊 Generando reportes estadísticos desde RDS...")


# -- QUERY 1: Total spent per month (only real checkins) --

query_mes = """
SELECT 
    TO_CHAR(fecha, 'YYYY-MM') AS mes,
    COUNT(*) AS total_asistencias,  -- Just real checkins
    SUM(precio_individual) AS gasto_total
FROM wellhub_trainings
WHERE tipo_registro = 'Checkin' AND estado = 'COMPLETED' 
GROUP BY mes
ORDER BY mes;
"""
df_mes = pd.read_sql(query_mes, conexion_url)

print("1. MONTHLY SPENDING IF PAID PER CLASS (ONLY REAL CHECKINS):")
print(df_mes.to_string(index=False))


# -- QUERY 2: TOP 5 GYMS BY SPENDING/USAGE --

query_gimnasios = """
SELECT 
    gimnasio,
    COUNT(*) AS visitas,
    SUM(precio_individual) AS gasto_gimnasio
FROM wellhub_trainings
WHERE estado = 'COMPLETED' AND tipo_registro = 'Checkin'
GROUP BY gimnasio
ORDER BY gasto_gimnasio DESC
LIMIT 5;
"""
df_gimnasios = pd.read_sql(query_gimnasios, conexion_url)

print("2. TOP 5 GYMS BY SPENDING:")
print(df_gimnasios.to_string(index=False))


# -- QUERY 3: ASSISTANCE RATIO (Checkin vs Booking vs Cancelled) --
query_ratio = """
SELECT 
    tipo_registro,
    estado,
    COUNT(*) AS cantidad,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS porcentaje
FROM wellhub_trainings
GROUP BY tipo_registro, estado
ORDER BY cantidad DESC;
"""
df_ratio = pd.read_sql(query_ratio, conexion_url)

print("3. ASSISTANCE AND BOOKING RATIO:")
print(df_ratio.to_string(index=False))