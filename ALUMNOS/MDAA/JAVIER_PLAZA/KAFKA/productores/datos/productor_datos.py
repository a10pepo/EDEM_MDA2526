from confluent_kafka import Producer
import pandas as pd
import json
import time

# Definir función para enviar los datos.
def enviar_datos(accion, precio, ma20, fecha):
    texto = f"El día {fecha}, la {accion} tiene un valor de {precio}$, y una MA(20) de {ma20}"
    mensaje = {
        "accion": accion, 
        "precio": precio,
        "ma20": ma20,
        "fecha": fecha
    }
    productor.produce(
        topic = "datos",
        value = json.dumps(mensaje).encode("utf-8")
    )
    print("Datos enviados:", texto)

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

# Eliminar las primeras 20 filas.
df = df.iloc[20:]

# Bucle para generar los datos y enviarlos al topico.
for _, fila in df.iterrows():
    fecha = fila["Date"]
    enviar_datos("Bitcoin", fila["BITCOIN"], fila["BITCOIN_ma20"], fecha)
    enviar_datos("Oro", fila["Gold"], fila["Gold_ma20"], fecha)
    time.sleep(1)

productor.flush()
