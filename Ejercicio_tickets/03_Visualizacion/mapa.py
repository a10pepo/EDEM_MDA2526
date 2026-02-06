import pandas as pd
import plotly.graph_objects as go

# 1. Cargamos los datos del archivo CSV

df = pd.read_csv('tickets.csv')

# Create sample coordinates if the CSV lacks lat/lon columns.
if 'latitud' not in df.columns or 'longitud' not in df.columns:
    base_lat = 39.4699  # Valencia center
    base_lon = -0.3763
    offsets = [(i % 5, i // 5) for i in range(len(df))]
    df['latitud'] = [base_lat + (dx - 2) * 0.01 for dx, dy in offsets]
    df['longitud'] = [base_lon + (dy - 2) * 0.01 for dx, dy in offsets]

# 2. Creamos la figura
fig = go.Figure(go.Scattermap(
    lat=df['latitud'],
    lon=df['longitud'],
    mode='markers',
    marker=go.scattermap.Marker(
        size=[max(10, p / 10) for p in df['precio']],
        color=df['precio'],
        colorscale='Viridis',
        showscale=True
    ),
    
    # El nombre principal que aparece
    text=df['tienda'],
    
    # 'customdata' almacena las columnas extra que queremos mostrar en el hover
    customdata=df[['fecha_compra', 'precio', 'id_ticket']],
    
    # Configuramos la etiqueta flotante (Hover)
    hovertemplate=(
        "<b>Tienda:</b> %{text}<br>" +
        "<b>Fecha:</b> %{customdata[0]}<br>" +
        "<b>Precio:</b> $%{customdata[1]:.2f}<br>" +
        "<b>id_ticket:</b> %{customdata[2]}" +
        "<extra></extra>"
    )
))

# 3. Configuración del diseño del mapa
fig.update_layout(
    title="Mapa de Ventas por Ubicación",
    autosize=True,
    hovermode='closest',
    map=dict(
        style="carto-positron", # Estilo elegante y gratuito
        bearing=0,
        center=dict(lat=df['latitud'].mean(), lon=df['longitud'].mean()),
        pitch=0,
        zoom=5
    ),
)

fig.show()
