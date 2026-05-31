from confluent_kafka import Producer
import pandas as pd
import json
import time

# Definir función para enviar las señales de compra o de venta.
def enviar_alerta(accion, alerta, precio, ma20, fecha):
    texto = f"El día {fecha}, se realizo la acción {alerta} sobre {accion} con un valor de {precio}$"
    mensaje = {
        "accion": accion, 
        "alerta": alerta,
        "precio": precio,
        "ma20": ma20,
        "fecha": fecha
    }
    productor.produce(
        topic = "alertas",
        value = json.dumps(mensaje).encode("utf-8")
    )
    print("Señal enviada:", texto)

# Configurar el productor.
config = {
    'bootstrap.servers': 'kafka:29092'
}
productor = Producer(config)

# Leer el csv y pasarlo a un dataframe.
df = pd.read_csv("SP500_oil_gold_bitcoin.csv")

# Eliminar columnas que no nos interesan.
df = df.drop(['Brent Oil', 'Crude Oil WTI', 'S&P500'], axis=1)

# Calcular la media movil de 20 dias de BTC y Oro.
df['BITCOIN_ma20'] = df['BITCOIN'].rolling(window=20).mean()
df['Gold_ma20'] = df['Gold'].rolling(window=20).mean() 

# Calcular valores previos para comparar
df['BITCOIN_prev'] = df['BITCOIN'].shift(1)
df['BITCOIN_ma20_prev'] = df['BITCOIN_ma20'].shift(1)
df['Gold_prev'] = df['Gold'].shift(1)
df['Gold_ma20_prev'] = df['Gold_ma20'].shift(1)

# Eliminar las primeras 20 filas (donde ma20 es NaN)
df = df.iloc[20:]

# Bucle para generar las alertas y enviarlas al topico.
for _, fila in df.iterrows():
    fecha = fila["Date"]
    if fila["BITCOIN"] == fila["BITCOIN_ma20"] and fila["BITCOIN_prev"] < fila["BITCOIN_ma20_prev"]:
        enviar_alerta("Bitcoin", "Compra", fila["BITCOIN"], fila["BITCOIN_ma20"], fecha)
    elif fila["BITCOIN"] == fila["BITCOIN_ma20"] and fila["BITCOIN_prev"] > fila["BITCOIN_ma20_prev"]:
        enviar_alerta("Bitcoin", "Venta", fila["BITCOIN"], fila["BITCOIN_ma20"], fecha)
    if fila["Gold"] == fila["Gold_ma20"] and fila["Gold_prev"] < fila["Gold_ma20_prev"]:
        enviar_alerta("Oro", "Compra", fila["Gold"], fila["Gold_ma20"], fecha)
    elif fila["Gold"] == fila["Gold_ma20"] and fila["Gold_prev"] > fila["Gold_ma20_prev"]:
        enviar_alerta("Oro", "Venta", fila["Gold"], fila["Gold_ma20"], fecha)
    time.sleep(1)

productor.flush()