import dash
from dash import dcc, html, Input, Output
from dash import dash_table
import psycopg2
import plotly.graph_objs as go

# -----------------------------
# Función para obtener datos
# -----------------------------
def get_valenbisi_data():
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            dbname="pruebadb",
            user="postgres",
            password="postgres",
            host="valenbisi_postgres",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT ON (address) address, "number", open, available, free, total, updated_at
            FROM public.valenbisi
            ORDER BY address, updated_at DESC
        """)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        data = [dict(zip(columns, row)) for row in rows]
        return data
    except Exception as e:
        print(e)
        return []
    finally:
        if cur: cur.close()
        if conn: conn.close()

# -----------------------------
# Inicializamos Dash
# -----------------------------
app = dash.Dash(__name__)

# -----------------------------
# Layout
# -----------------------------
app.layout = html.Div([
    html.H1("🚲 Valenbisi Dashboard Dinámico", style={'textAlign': 'center', 'color': '#ff1493'}),

    dcc.Interval(id='interval', interval=10*1000, n_intervals=0),
    dcc.Store(id='data-store'),

    # KPIs generales
    html.Div(id='kpi-container', style={'display': 'flex', 'justifyContent': 'space-around', 'marginTop': '20px'}),

    # Tablas dinámicas
    html.H2("Top 10 estaciones con mayor disponibilidad", style={'textAlign': 'center', 'marginTop': '40px'}),
    dash_table.DataTable(
        id='top-availability-table',
        page_size=10,
        sort_action="native",
        style_table={'margin': '0 auto', 'width': '80%'},
        style_cell={'textAlign': 'center', 'fontFamily': 'Arial'}
    ),
    
    html.H2("Top 10 estaciones con menor disponibilidad", style={'textAlign': 'center', 'marginTop': '40px'}),
    dash_table.DataTable(
        id='bottom-availability-table',
        page_size=10,
        sort_action="native",
        style_table={'margin': '0 auto', 'width': '80%'},
        style_cell={'textAlign': 'center', 'fontFamily': 'Arial'}
    ),

    # Gráfico de disponibilidad
    html.H2("Tasa de disponibilidad (%) de todas las estaciones", style={'textAlign': 'center', 'marginTop': '40px'}),
    dcc.Graph(id='availability-rate-graph'),

    # Tabla dinámica de espacios libres
    html.H2("Top 10 estaciones con más espacios libres", style={'textAlign': 'center', 'marginTop': '40px'}),
    dash_table.DataTable(
        id='top-free-table',
        page_size=10,
        sort_action="native",
        style_table={'margin': '0 auto', 'width': '80%'},
        style_cell={'textAlign': 'center', 'fontFamily': 'Arial'}
    ),

    # Gráfico de espacios libres
    html.H2("Tasa de espacios libres (%) de todas las estaciones", style={'textAlign': 'center', 'marginTop': '40px'}),
    dcc.Graph(id='free-rate-graph'),

], style={'backgroundColor': '#fff0f5', 'minHeight': '100vh', 'padding': '20px'})

# -----------------------------
# Callback: actualizar datos
# -----------------------------
@app.callback(
    Output('data-store', 'data'),
    Input('interval', 'n_intervals')
)
def update_data(n):
    return get_valenbisi_data()

# -----------------------------
# Callback: KPIs generales
# -----------------------------
@app.callback(
    Output('kpi-container', 'children'),
    Input('data-store', 'data')
)
def update_kpis(data):
    if not data:
        return []
    total_bicis = sum(d['available'] for d in data)
    total_espacios = sum(d['free'] for d in data)
    mas_llena = max(data, key=lambda x: x['available'])
    mas_vacia = min(data, key=lambda x: x['available'])

    kpi_style = {'padding': '20px', 'backgroundColor': '#ff69b4', 'borderRadius': '10px', 'color': 'white',
                 'textAlign': 'center', 'width': '200px', 'boxShadow': '0 4px 8px rgba(0,0,0,0.2)'}
    return [
        html.Div([html.H4("Total Bicis 🚲"), html.H3(f"{total_bicis}")], style=kpi_style),
        html.Div([html.H4("Total Espacios 🅿️"), html.H3(f"{total_espacios}")], style=kpi_style),
        html.Div([html.H4("Estación Más Llena"), html.P(f"{mas_llena['address']} ({mas_llena['available']}/{mas_llena['total']})")], style=kpi_style),
        html.Div([html.H4("Estación Más Vacía"), html.P(f"{mas_vacia['address']} ({mas_vacia['available']}/{mas_vacia['total']})")], style=kpi_style)
    ]

# -----------------------------
# Callback: tablas dinámicas de disponibilidad
# -----------------------------
@app.callback(
    Output('top-availability-table', 'data'),
    Output('top-availability-table', 'columns'),
    Output('bottom-availability-table', 'data'),
    Output('bottom-availability-table', 'columns'),
    Input('data-store', 'data')
)
def update_tables(data):
    if not data:
        return [], [], [], []

    for d in data:
        d['% Ocupación'] = round(d['available']/d['total']*100,1) if d['total'] else 0

    top10 = sorted(data, key=lambda x: x['available']/x['total'], reverse=True)[:10]
    bottom10 = sorted(data, key=lambda x: x['available']/x['total'])[:10]

    columns = [{"name": c, "id": c} for c in ["address","available","free","total","% Ocupación","updated_at"]]

    return top10, columns, bottom10, columns

# -----------------------------
# Callback: gráfico de disponibilidad
# -----------------------------
@app.callback(
    Output('availability-rate-graph', 'figure'),
    Input('data-store', 'data')
)
def update_availability_graph(data):
    if not data:
        return go.Figure()
    addresses = [d['address'] for d in data]
    rates = [round(d['available']/d['total']*100,1) if d['total'] else 0 for d in data]
    colors = ['#00cc96' if r>70 else '#ffa500' if r>30 else '#ff4136' for r in rates]

    fig = go.Figure([go.Bar(x=addresses, y=rates, marker_color=colors)])
    fig.update_layout(xaxis_tickangle=-45, yaxis_title="Disponibilidad (%)", plot_bgcolor='#fff0f5', paper_bgcolor='#fff0f5')
    return fig

# -----------------------------
# Callback: tabla dinámica de espacios libres
# -----------------------------
@app.callback(
    Output('top-free-table', 'data'),
    Output('top-free-table', 'columns'),
    Input('data-store', 'data')
)
def update_free_table(data):
    if not data:
        return [], []

    for d in data:
        d['% Espacios libres'] = round(d['free']/d['total']*100,1) if d['total'] else 0

    top_free = sorted(data, key=lambda x: x['free']/x['total'], reverse=True)[:10]

    columns = [{"name": c, "id": c} for c in ["address","free","total","% Espacios libres","updated_at"]]

    return top_free, columns

# -----------------------------
# Callback: gráfico de espacios libres
# -----------------------------
@app.callback(
    Output('free-rate-graph', 'figure'),
    Input('data-store', 'data')
)
def update_free_graph(data):
    if not data:
        return go.Figure()

    addresses = [d['address'] for d in data]
    free_rates = [round(d['free']/d['total']*100,1) if d['total'] else 0 for d in data]
    colors = ['#00cc96' if r>70 else '#ffa500' if r>30 else '#ff4136' for r in free_rates]

    fig = go.Figure([go.Bar(x=addresses, y=free_rates, marker_color=colors)])
    fig.update_layout(xaxis_tickangle=-45, yaxis_title="Espacios libres (%)", plot_bgcolor='#fff0f5', paper_bgcolor='#fff0f5')
    return fig

# -----------------------------
# Ejecutar app
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
