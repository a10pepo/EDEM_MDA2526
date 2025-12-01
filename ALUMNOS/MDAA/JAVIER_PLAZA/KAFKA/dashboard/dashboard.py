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

# Función para que se consuman datos de la tabla creada con ksql en el archivo crear_tabla.sql
def consumir_ksql():
    config = {
        "bootstrap.servers": "kafka:29092",
        "group.id": "grupo_contador",
        "auto.offset.reset": "earliest"
    }
    consumidor = Consumer(config)
    consumidor.subscribe(["contar_senales"])
    print(" Dashboard conectado a la tabla contar_senales")
    while True:
        mensaje = consumidor.poll(1.0)
        if mensaje is None:
            continue
        if mensaje.error():
            print(f"Error al recibir mensaje: {mensaje.error()}")
            continue
        try:
            payload = json.loads(mensaje.value().decode("utf-8"))
        except Exception as e:
            print("Erro decodificando el JSON:", e)
            print("Mensaje en bruto:", mensaje.value())
            continue
        accion = payload.get("accion")
        senal = payload.get("senal")
        total = payload.get("total")
        if accion is None or senal is None or total is None:
            continue
        resultados[(accion, senal)] = total

# Para que el progama únicamente no ejecute la función comsumir_ksql, se le pone esto para que la ejecute al mismo tiempo que se hace el dashboard, diciendole al programa que la función es secundaria. Siendo la función principal la que haga el dashboard. 
hilo = Thread(target=consumir_ksql, daemon=True)
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