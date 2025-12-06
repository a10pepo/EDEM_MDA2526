# dashboard.py
from dash import Dash, dcc, html
import psycopg
import plotly.express as px
import time

app = Dash(__name__)

# Configuración de conexión
DB_CONFIG = {
    "host": "postgres",
    "port": 5432,
    "dbname": "pruebadb",
    "user": "postgres",
    "password": "postgres"
}

# Función para obtener datos con reintentos infinitos
def fetch_data(table_name, query_columns):
    while True:
        try:
            with psycopg.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT {', '.join(query_columns)} FROM {table_name};")
                    rows = cur.fetchall()
                    return [dict(zip(query_columns, r)) for r in rows]
        except psycopg.errors.UndefinedTable:
            print(f"Tabla {table_name} no encontrada. Esperando 2 segundos...")
            time.sleep(2)

# Datos de las tablas
stations = fetch_data("mart_valenbisi", ["address", "available", "total"])
summary = fetch_data("mart_summary", ["metric", "value"])
time_summary = fetch_data("mart_time_summary", ["time_period", "value"])

# Crear figuras
fig_stations = px.bar(stations, x="address", y="available", title="Bicicletas disponibles por estación")
fig_summary = px.bar(summary, x="metric", y="value", title="Resumen de métricas")
fig_time = px.line(time_summary, x="time_period", y="value", title="Resumen temporal")

# Layout de Dash con varias gráficas
app.layout = html.Div([
    html.H1("Dashboard Valenbisi"),
    dcc.Graph(figure=fig_stations),
    dcc.Graph(figure=fig_summary),
    dcc.Graph(figure=fig_time)
])

# Ejecutar servidor
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050)
