import requests
from dash import Dash, dcc, html
import plotly.graph_objects as go
from dash.dependencies import Output, Input
import time

# URL de tu API
API_URL = "http://api_get_post:8000/stations"

# Función para obtener datos de la API con reintentos
def fetch_stations(limit=100, retries=10, delay=3):
    for i in range(retries):
        try:
            response = requests.get(API_URL, params={"limit": limit})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Intento {i+1}: Error al obtener datos: {e}")
            time.sleep(delay)
    return []

# Crear app Dash
app = Dash(__name__)

# Layout de Dash
app.layout = html.Div([
    html.H1("Dashboard Valenbisi"),
    dcc.Graph(id="bici-graph"),
    dcc.Interval(id="interval-component", interval=30*1000, n_intervals=0)  # Actualiza cada 30s
])

# Callback para actualizar el gráfico
@app.callback(
    Output("bici-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_graph(n):
    stations = fetch_stations()
    if not stations:
        stations = [{"address": "Sin datos", "available": 0, "total": 0, "fetched_at": ""}]

    addresses = [s["address"] for s in stations]
    available = [s["available"] for s in stations]
    total = [s["total"] for s in stations]
    fetched_at = [s.get("fetched_at", "") for s in stations]

    fig = go.Figure(
        data=[go.Bar(
            x=addresses,
            y=available,
            text=[f"Total: {t}<br>Fecha: {f}" for t, f in zip(total, fetched_at)],
            hoverinfo='text'
        )],
        layout=go.Layout(
            title="Bicicletas disponibles por estación",
            xaxis_title="Estación",
            yaxis_title="Disponibles"
        )
    )
    return fig

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)
