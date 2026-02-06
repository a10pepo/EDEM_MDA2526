import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dash import Dash, html, dcc
import os

# ── Cargar datos ──────────────────────────────────────────────────────────────

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "tickets.csv")
df = pd.read_csv(csv_path)

# Assign spending categories based on store name.
categoria_map = {
    "Mercadona": "alimentacion",
    "Carrefour": "alimentacion",
    "Gasolinera Repsol": "alimentacion",
    "Restaurante El Pescador": "alimentacion",
    "Starbucks": "alimentacion",
    "Burger King": "alimentacion",
    "Farmacia Central": "alimentacion",
    "Zara": "ropa",
    "H&M": "ropa",
    "Decathlon": "ropa",
    "Netflix": "ocio",
    "Cines Yelmo": "ocio",
    "Amazon": "tecnologia",
    "Apple Store": "tecnologia",
    "MediaMarkt": "tecnologia",
    "IKEA": "tecnologia",
}
df["categoria"] = df["tienda"].map(categoria_map).fillna("ocio")

if "latitud" not in df.columns or "longitud" not in df.columns:
    base_lat, base_lon = 39.4699, -0.3763
    offsets = [(i % 5, i // 5) for i in range(len(df))]
    df["latitud"] = [base_lat + (dx - 2) * 0.01 for dx, _ in offsets]
    df["longitud"] = [base_lon + (dy - 2) * 0.01 for _, dy in offsets]


# ── 1. Mapa ───────────────────────────────────────────────────────────────────

def crear_mapa(df):
    fig = go.Figure(go.Scattermap(
        lat=df["latitud"],
        lon=df["longitud"],
        mode="markers",
        marker=go.scattermap.Marker(
            size=[max(10, p / 10) for p in df["precio"]],
            color=df["precio"],
            colorscale="Viridis",
            showscale=True,
        ),
        text=df["tienda"],
        customdata=df[["fecha_compra", "precio", "id_ticket"]],
        hovertemplate=(
            "<b>Tienda:</b> %{text}<br>"
            "<b>Fecha:</b> %{customdata[0]}<br>"
            "<b>Precio:</b> %{customdata[1]:.2f} EUR<br>"
            "<b>ID:</b> %{customdata[2]}"
            "<extra></extra>"
        ),
    ))
    fig.update_layout(
        title="Mapa de Ventas por Ubicacion",
        autosize=True,
        hovermode="closest",
        height=600,
        map=dict(
            style="carto-positron",
            bearing=0,
            center=dict(lat=df["latitud"].mean(), lon=df["longitud"].mean()),
            pitch=0,
            zoom=5,
        ),
    )
    return fig


# ── 2. Dashboard de graficas ──────────────────────────────────────────────────

def crear_dashboard(df):
    df = df.copy()
    df["fecha_compra"] = pd.to_datetime(df["fecha_compra"])
    df = df.sort_values("fecha_compra")

    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            "Gasto por Fecha",
            "Gasto por Tienda",
            "Top Tiendas por Gasto Total",
            "Distribucion de Precios",
            "Timeline de Compras",
            "Numero de Compras por Tienda",
        ),
        specs=[
            [{"type": "bar"}, {"type": "pie"}],
            [{"type": "bar"}, {}],
            [{"type": "scatter"}, {"type": "bar"}],
        ],
        vertical_spacing=0.10,
        horizontal_spacing=0.08,
    )

    # 1) Gasto por fecha
    gasto_fecha = df.groupby("fecha_compra")["precio"].sum().reset_index()
    fig.add_trace(
        go.Bar(x=gasto_fecha["fecha_compra"], y=gasto_fecha["precio"],
            marker_color="#3498db", showlegend=False),
        row=1, col=1,
    )

    # 2) Gasto por tienda (donut)
    gasto_tienda = df.groupby("tienda")["precio"].sum()
    fig.add_trace(
        go.Pie(
            labels=gasto_tienda.index, values=gasto_tienda.values,
            hole=0.45, textinfo="label+percent", showlegend=False,
        ),
        row=1, col=2,
    )


    # 3) Gasto por categoria
    gasto_categoria = df.groupby("categoria")["precio"].sum().reindex(
        ["ropa", "ocio", "alimentacion", "tecnologia"], fill_value=0
    )
    fig.add_trace(
        go.Bar(
            x=gasto_categoria.index,
            y=gasto_categoria.values,
            marker_color="#e67e22",
            showlegend=False,
        ),
        row=2,
        col=2,
    )

    # 4) Top tiendas por gasto total
    top_tiendas = df.groupby("tienda")["precio"].sum().sort_values(ascending=True)
    fig.add_trace(
        go.Bar(x=top_tiendas.values, y=top_tiendas.index, orientation="h",
            marker_color="#2ecc71", showlegend=False),
        row=2, col=1,
    )


    fig.update_layout(
        title=dict(text="Dashboard de Tickets de Compra", font=dict(size=22)),
        height=1100,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Segoe UI, sans-serif", size=12),
    )
    fig.update_yaxes(title_text="EUR", row=1, col=1)
    fig.update_yaxes(title_text="EUR", row=3, col=1)
    fig.update_xaxes(tickangle=-45, row=3, col=2)

    # KPIs
    total_gastado = df["precio"].sum()
    media_ticket = df["precio"].mean()
    ticket_max = df["precio"].max()
    num_tickets = len(df)
    fig.add_annotation(
        text=(
            f"<b>Total gastado:</b> {total_gastado:,.2f} EUR  |  "
            f"<b>Ticket medio:</b> {media_ticket:,.2f} EUR  |  "
            f"<b>Ticket max:</b> {ticket_max:,.2f} EUR  |  "
            f"<b>Num. tickets:</b> {num_tickets}"
        ),
        xref="paper", yref="paper", x=0.5, y=-0.04,
        showarrow=False, font=dict(size=14),
    )
    return fig


# ── 3. Tabla ──────────────────────────────────────────────────────────────────

def crear_tabla(df):
    df = df.copy()
    df = df.sort_values("fecha_compra")
    n = len(df)
    row_colors = ["#f2f2f2" if i % 2 == 0 else "white" for i in range(n)]
    precio_formatted = [f"{p:.2f} EUR" for p in df["precio"]]

    fig = go.Figure(
        go.Table(
            header=dict(
                values=["ID Ticket", "Fecha Compra", "Tienda", "Precio"],
                fill_color="#2c3e50",
                font=dict(color="white", size=13),
                align="center",
            ),
            cells=dict(
                values=[
                    df["id_ticket"].tolist(),
                    df["fecha_compra"].tolist(),
                    df["tienda"].tolist(),
                    precio_formatted,
                ],
                fill_color=[row_colors] * 4,
                align=["center", "center", "left", "right"],
                font=dict(size=12),
                height=30,
            ),
        )
    )
    fig.update_layout(
        title="Detalle de Tickets",
        height=max(400, 45 * n),
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


# ── App Dash ──────────────────────────────────────────────────────────────────

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Tickets de Compra", style={"textAlign": "center", "padding": "20px"}),
    dcc.Graph(id="mapa", figure=crear_mapa(df)),
    html.Hr(),
    dcc.Graph(id="dashboard", figure=crear_dashboard(df)),
    html.Hr(),
    dcc.Graph(id="tabla", figure=crear_tabla(df)),
], style={"maxWidth": "1400px", "margin": "0 auto"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
