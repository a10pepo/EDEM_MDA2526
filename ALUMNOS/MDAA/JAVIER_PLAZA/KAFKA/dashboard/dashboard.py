from confluent_kafka import Consumer
import json
from threading import Thread
import dash
from dash import html, dcc
import plotly.graph_objs as go

# Diccionario inicial de la cuenta de las compras y las ventas
resultados = {
    ("Bitcoin", "Compra"): 0,
    ("Bitcoin", "Venta"): 0,
    ("Oro", "Compra"): 0,
    ("Oro", "Venta"): 0,
}

# Función para que se consuman datos directamente del topic 'senales'
def consumir_datos():
    config = {
        "bootstrap.servers": "kafka:29092",
        "group.id": "grupo_dashboard_contador",
        "auto.offset.reset": "earliest"
    }
    consumidor = Consumer(config)
    consumidor.subscribe(["senales"])
    print(" Dashboard conectado al topic 'senales'")
    while True:
        mensaje = consumidor.poll(1.0)
        if mensaje is None:
            continue
        if mensaje.error():
            print(f"Error al recibir mensaje: {mensaje.error()}")
            continue
        try:
            payload = json.loads(mensaje.value().decode("utf-8"))
            
            accion = payload.get("accion")
            senal = payload.get("senal")
            
            if accion and senal:
                # Normalizar claves si es necesario (el productor manda "Compra"/"Venta" y "Bitcoin"/"Oro")
                key = (accion, senal)
                if key in resultados:
                    resultados[key] += 1
                    # print(f"Actualizado: {key} -> {resultados[key]}")
                else:
                    print(f"Clave desconocida: {key}")
                    
        except Exception as e:
            print("Error procesando mensaje:", e)
            continue

# Ejecutar el consumidor en un hilo separado
hilo = Thread(target=consumir_datos, daemon=True)
hilo.start()

# Creación de la aplicación donde se verá el dashboard.
app = dash.Dash(__name__)

# Definir el contenido de la página donde se ve el dashboard
app.layout = html.Div([
    html.H1("Dashboard financiero con Kafka y Plotly"),
    dcc.Graph(id="grafico_contador"),
    dcc.Interval(id="intervalo", interval=1000, n_intervals=0)
])

# Actualización del gráfico en función de las entradas en la tabla de KSQL
@app.callback(
    dash.Output("grafico_contador", "figure"),
    [dash.Input("intervalo", "n_intervals")]
)
def actualizar(_):
    etiquetas = []
    valores = []
    for (accion, senal), total in resultados.items():
        etiquetas.append(f"{accion}-{senal}")
        valores.append(total)
    figura = go.Figure([go.Bar(x=etiquetas, y=valores)])
    figura.update_layout(
        title="Órdenes ejecutadas (streaming desde KSQL)",
        xaxis_title="Señal",
        yaxis_title="Total",
        template="plotly_dark"
    )
    return figura

# Manda los gráficos a la "página web"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)