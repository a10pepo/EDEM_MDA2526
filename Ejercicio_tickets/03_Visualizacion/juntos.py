import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, dash_table, Input, Output
import requests

# --- 1. FUNCIÓN PARA CARGAR DATOS (CENTRALIZADA) ---
def cargar_datos():
    url = "http://localhost:8000/datos"
    try:
        print(f"Intentando conectar a {url}...")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception as e:
        print(f"Error conectando al backend: {e}")
        return pd.DataFrame()

# --- 2. FUNCIONES DE VISUALIZACIÓN ---
def crear_mapa(df):
    if df.empty: return go.Figure()
    fig = go.Figure(go.Scattermap(
        lat=df["latitud"], lon=df["longitud"],
        mode="markers",
        marker=go.scattermap.Marker(size=12, color=df["precio"], colorscale="Viridis", showscale=True),
        text=df["tienda"]
    ))
    fig.update_layout(
        title="Ubicación de Compras",
        height=400,
        map=dict(style="carto-positron", center=dict(lat=df["latitud"].mean(), lon=df["longitud"].mean()), zoom=4),
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    return fig

def crear_dashboard(df):
    if df.empty: return go.Figure()
    df["fecha_compra"] = pd.to_datetime(df["fecha_compra"])
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Gasto por Fecha", "Distribución por Tienda"), specs=[[{"type": "bar"}, {"type": "pie"}]])
    
    gasto_fecha = df.groupby("fecha_compra")["precio"].sum().reset_index()
    fig.add_trace(go.Bar(x=gasto_fecha["fecha_compra"], y=gasto_fecha["precio"], marker_color="#3498db"), row=1, col=1)
    
    gasto_tienda = df.groupby("tienda")["precio"].sum()
    fig.add_trace(go.Pie(labels=gasto_tienda.index, values=gasto_tienda.values, hole=.3), row=1, col=2)
    
    fig.update_layout(height=400, showlegend=False, template="plotly_white")
    return fig

# --- 3. CONFIGURACIÓN DE LA APP ---
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Tickets (Actualización Automática)", style={"textAlign": "center"}),
    
    # El componente Interval: 60*1000 milisegundos = 1 minuto
    dcc.Interval(
        id='intervalo-actualizacion',
        interval=60*1000, 
        n_intervals=0
    ),

    html.Div(id='indicador-kpis', style={"display": "flex", "justifyContent": "center", "gap": "20px"}),
    
    dcc.Graph(id='grafico-mapa'),
    dcc.Graph(id='grafico-principal'),
    
    html.H3("Listado de Tickets"),
    dash_table.DataTable(
        id='tabla-tickets',
        columns=[
            {"name": "ID Ticket", "id": "id_ticket"},
            {"name": "Fecha", "id": "fecha_compra"},
            {"name": "Tienda", "id": "tienda"},
            {"name": "Precio", "id": "precio"}
        ],
        page_size=10,
        style_cell={'textAlign': 'left', 'padding': '10px'}
    )
], style={"maxWidth": "1200px", "margin": "0 auto", "padding": "20px"})

# --- 4. CALLBACK DE ACTUALIZACIÓN ---
@app.callback(
    [Output('grafico-mapa', 'figure'),
    Output('grafico-principal', 'figure'),
    Output('tabla-tickets', 'data'),
    Output('indicador-kpis', 'children')],
    [Input('intervalo-actualizacion', 'n_intervals')]
)
def actualizar_todo(n):
    # Esta función se ejecuta al cargar la página y cada 60 segundos
    df = cargar_datos()
    
    if df.empty:
        return go.Figure(), go.Figure(), [], "No hay datos disponibles"

    # Generar nuevas figuras con los datos frescos
    fig_mapa = crear_mapa(df)
    fig_dash = crear_dashboard(df)
    datos_tabla = df.to_dict('records')
    
    # Crear KPIs
    kpis = [
        html.Div([html.B("Total: "), f"{df['precio'].sum():.2f} EUR"]),
        html.Div([html.B("Tickets: "), f"{len(df)}"]),
        html.Div([html.Small(f"Última actualización: {pd.Timestamp.now().strftime('%H:%M:%S')}")], style={"color": "gray"})
    ]
    
    return fig_mapa, fig_dash, datos_tabla, kpis

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
