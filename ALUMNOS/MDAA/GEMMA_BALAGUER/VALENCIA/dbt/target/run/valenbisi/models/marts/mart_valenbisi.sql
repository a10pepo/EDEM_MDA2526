
  create view "pruebadb"."public"."mart_valenbisi__dbt_tmp"
    
    
  as (
    import time
import psycopg2
from psycopg2.extras import RealDictCursor
from dash import Dash, dcc, html, Input, Output

# -------------------------
# Conexión con reintentos
# -------------------------
def get_connection():
    while True:
        try:
            conn = psycopg2.connect(
                host="valenbisi_postgres",
                database="pruebadb",
                user="postgres",
                password="postgres",
                port=5432
            )
            print("✅ Conectado a PostgreSQL")
            return conn
        except psycopg2.OperationalError:
            print("⏳ PostgreSQL no está listo, reintentando en 2s...")
            time.sleep(2)

conn = get_connection()

def fetch(query, params=None):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchall()

# -------------------------
# Dropdown estaciones
# -------------------------
QUERY_STATIONS = """
SELECT address
FROM mart_valenbisi
ORDER BY address;
"""

stations = fetch(QUERY_STATIONS)
station_options = [
    {"label": s["address"], "value": s["address"]}
    for s in stations
]

# -------------------------
# App Dash
# -------------------------
app = Dash(__name__)

app.layout = html.Div(
    style={"padding": "20px"},
    children=[
        html.H1("Dashboard Valenbisi 🚲", style={"color": "#800080"}),

        dcc.Dropdown(
            id="station-dropdown",
            options=station_options,
            placeholder="Selecciona una estación"
        ),

        dcc.Graph(id="availability-bar"),

        html.Div(id="kpi-available"),
        html.Div(id="kpi-occupancy")
    ]
)

# -------------------------
# Callback
# -------------------------
@app.callback(
    Output("availability-bar", "figure"),
    Output("kpi-available", "children"),
    Output("kpi-occupancy", "children"),
    Input("station-dropdown", "value")
)
def update_dashboard(address):

    query = """
    SELECT address, available, total
    FROM mart_valenbisi
    {}
    """

    if address:
        rows = fetch(query.format("WHERE address = %s"), (address,))
    else:
        rows = fetch(query.format(""))

    addresses = [r["address"] for r in rows]
    available = [r["available"] for r in rows]
    total = [r["total"] for r in rows]

    figure = {
        "data": [
            {"x": addresses, "y": available, "type": "bar", "name": "Disponibles"},
            {"x": addresses, "y": total, "type": "bar", "name": "Capacidad"}
        ],
        "layout": {
            "title": "Disponibilidad por estación",
            "barmode": "group"
        }
    }

    total_available = sum(available)
    total_capacity = sum(total)
    occupancy = round((total_available / total_capacity) * 100, 2) if total_capacity else 0

    return (
        figure,
        f"🚲 Bicis disponibles: {total_available}",
        f"📊 Ocupación: {occupancy}%"
    )

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
  );