from dash import Dash, dcc, html
import psycopg
import plotly.express as px
import time

app = Dash(__name__)

DB_CONFIG = {
    "host": "postgres",
    "port": 5432,
    "dbname": "pruebadb",
    "user": "postgres",
    "password": "postgres"
}

TABLE_NAME = "mart_valenbisi"

def fetch_data(retries=10, delay=2):
    for attempt in range(retries):
        try:
            with psycopg.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT address, available, total FROM {TABLE_NAME};")
                    rows = cur.fetchall()
                    return [{"address": r[0], "available": r[1], "total": r[2]} for r in rows]
        except psycopg.errors.UndefinedTable:
            print(f"Tabla {TABLE_NAME} no encontrada. Reintentando en {delay} segundos...")
            time.sleep(delay)
    raise RuntimeError(f"La tabla {TABLE_NAME} no se creó después de varios intentos.")

stations = fetch_data()
fig = px.bar(stations, x="address", y="available", title="Bicicletas disponibles por estación")
app.layout = html.Div([dcc.Graph(figure=fig)])

TABLE_NAME = "mart_summary"

def fetch_data_summary(retries=10, delay=2):
    for attempt in range(retries):
        try:
            with psycopg.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT metric, value FROM {TABLE_NAME};")
                    rows = cur.fetchall()
                    return [{"metric": r[0], "value": r[1]} for r in rows]
        except psycopg.errors.UndefinedTable:
            print(f"Tabla {TABLE_NAME} no encontrada. Reintentando en {delay} segundos...")
            time.sleep(delay)
    raise RuntimeError(f"La tabla {TABLE_NAME} no se creó después de varios intentos.")

summary = fetch_data_summary()
fig_summary = px.bar(summary, x="metric", y="value", title="Resumen de métricas")
app.layout = html.Div([dcc.Graph(figure=fig_summary)])

TABLE_NAME = "mart_time_summary"

def fetch_data_time(retries=10, delay=2):
    for attempt in range(retries):
        try:
            with psycopg.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT time_period, value FROM {TABLE_NAME};")
                    rows = cur.fetchall()
                    return [{"time_period": r[0], "value": r[1]} for r in rows]
        except psycopg.errors.UndefinedTable:
            print(f"Tabla {TABLE_NAME} no encontrada. Reintentando en {delay} segundos...")
            time.sleep(delay)
    raise RuntimeError(f"La tabla {TABLE_NAME} no se creó después de varios intentos.")

time_summary = fetch_data_time()
fig_time = px.line(time_summary, x="time_period", y="value", title="Resumen temporal")
app.layout = html.Div([dcc.Graph(figure=fig_time)])

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050)