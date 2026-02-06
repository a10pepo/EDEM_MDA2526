import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
from plotly.subplots import make_subplots


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
            labels=gasto_tienda.index,
            values=gasto_tienda.values,
            hole=0.45,
            textinfo="label+percent",
            showlegend=False,
        ),
        row=1, col=2,
    )

    # 3) Top tiendas por gasto total (horizontal bar)
    top_tiendas = df.groupby("tienda")["precio"].sum().sort_values(ascending=True)
    fig.add_trace(
        go.Bar(x=top_tiendas.values, y=top_tiendas.index, orientation="h",
            marker_color="#2ecc71", showlegend=False),
        row=2, col=1,
    )

    # 4) Distribucion de precios (histograma)
    fig.add_trace(
        go.Histogram(x=df["precio"], nbinsx=10,
                    marker_color="#9b59b6", showlegend=False),
        row=2, col=2,
    )

    # 5) Timeline de compras (scatter coloreado por tienda)
    colores = px.colors.qualitative.Set3 + px.colors.qualitative.Pastel
    for i, tienda in enumerate(df["tienda"].unique()):
        subset = df[df["tienda"] == tienda]
        fig.add_trace(
            go.Scatter(
                x=subset["fecha_compra"], y=subset["precio"],
                mode="markers",
                marker=dict(size=10, color=colores[i % len(colores)],
                            line=dict(width=1, color="white")),
                text=subset["id"] + "<br>" + subset["tienda"] + "<br>" + subset["precio"].astype(str) + " EUR",
                hoverinfo="text",
                name=tienda,
                showlegend=True,
            ),
            row=3, col=1,
        )

    # 6) Numero de compras por tienda
    compras_tienda = df["tienda"].value_counts().sort_values(ascending=False)
    fig.add_trace(
        go.Bar(x=compras_tienda.index, y=compras_tienda.values,
            marker_color="#e74c3c", showlegend=False),
        row=3, col=2,
    )

    # Layout
    fig.update_layout(
        title=dict(
            text="Dashboard de Tickets de Compra",
            font=dict(size=22),
        ),
        height=1100,
        width=1300,
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
        xref="paper", yref="paper",
        x=0.5, y=-0.04,
        showarrow=False,
        font=dict(size=14),
    )

    return fig


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
                    df["id"].tolist(),
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
        width=1000,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


if _name_ == "_main_":
    script_dir = os.path.dirname(os.path.abspath(_file_))
    csv_path = os.path.join(script_dir, "tickets.csv")

    df = pd.read_csv(csv_path)
    print(f"Cargados {len(df)} tickets de {df['tienda'].nunique()} tiendas")

    dashboard = crear_dashboard(df)
    tabla = crear_tabla(df)

    dashboard_path = os.path.join(script_dir, "dashboard_tickets.html")
    tabla_path = os.path.join(script_dir, "tabla_tickets.html")

    dashboard.write_html(dashboard_path, include_plotlyjs=True)
    tabla.write_html(tabla_path, include_plotlyjs=True)

    print(f"Dashboard guardado en '{dashboard_path}'")
    print(f"Tabla guardada en '{tabla_path}'")

    dashboard.show()
    tabla.show()