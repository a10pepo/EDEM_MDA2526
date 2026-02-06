import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('tickets.csv')

fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.id, df.fecha_compra, df.precio, df.direccion_establecimiento, df.nombre_tienda],
            fill_color='lavender',
            align='left'))
])

fig.show()