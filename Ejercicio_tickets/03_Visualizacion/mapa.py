import pandas as pd
import plotly.graph_objects as go

# 1. Cargamos los datos del archivo CSV
# Reemplaza 'compras.csv' por la ruta de tu archivo
df = pd.read_csv('tickets.csv')

# Create sample coordinates if the CSV lacks lat/lon columns.
if 'lat' not in df.columns or 'lon' not in df.columns:
    base_lat = 39.4699  # Valencia center
    base_lon = -0.3763
    # Spread points in a small grid around the center.
    offsets = [(i % 5, i // 5) for i in range(len(df))]
    df['lat'] = [base_lat + (dx - 2) * 0.01 for dx, dy in offsets]
    df['lon'] = [base_lon + (dy - 2) * 0.01 for dx, dy in offsets]

# 2. Creamos la figura
fig = go.Figure(go.Scattermap(
    lat=df['lat'],
    lon=df['lon'],
    mode='markers',
    marker=go.scattermap.Marker(
        size=12,
        # Opcional: El color cambia según el precio (escala de colores)
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
        center=dict(lat=df['lat'].mean(), lon=df['lon'].mean()), # Centrado automático
        pitch=0,
        zoom=11
    ),
)

fig.show()
