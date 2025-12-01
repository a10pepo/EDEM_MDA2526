from confluent_kafka import Producer
import time
import json
import pandas as pd

# Configuración del productor y creación del mismo. 
config = {
    'bootstrap.servers': 'kafka:29092'
}
productor = Producer(config)

# Definir función para enviar las señales de compra o de venta.
def enviar_mensaje(accion, senal, precio, ma20, fecha):
    texto = f"El día {fecha}, se {senal} {accion} con un valor de {precio}$"
    mensaje = {
        "accion": accion, 
        "senal": senal,
        "precio": precio,
        "ma20": ma20,
        "fecha": fecha
    }

    productor.produce(
        topic = "senales",
        value = json.dumps(mensaje).encode("utf-8")
    )
    print("Señal enviada:", texto)


# Descargar los datos de kaggle y pasarlos a un dataframe con pandas.
df = pd.read_csv("SP500_oil_gold_bitcoin.csv")


# Eliminar las columnas que no nos interesan. 
df = df.drop(['Brent Oil', 'Crude Oil WTI', 'S&P500'], axis=1)

# Calculo de la media movil a 20 días de BTC y Oro.
df['BITCOIN_ma20'] = df['BITCOIN'].rolling(window=20).mean()
df['Gold_ma20'] = df['Gold'].rolling(window=20).mean()

# Eliminar 20 primeras filas 
df = df.iloc[20:]

# bucle para la generación de las alertas. 
for _, fila in df.iterrows():
    fecha = fila["Date"]
    if fila["BITCOIN"] > fila["BITCOIN_ma20"]:
        enviar_mensaje("Bitcoin", "Comprar", fila["BITCOIN"], fila["BITCOIN_ma20"], fecha)
    elif fila["BITCOIN"] < fila["BITCOIN_ma20"]:
        enviar_mensaje("Bitcion", "Vender", fila["BITCOIN"], fila["BITCOIN_ma20"], fecha)
    if fila["Gold"] > fila["Gold_ma20"]:
        enviar_mensaje("Oro", "Comprar", fila["Gold"], fila["Gold_ma20"], fecha)
    elif fila["Gold"] < fila["Gold_ma20"]:
        enviar_mensaje("Oro", "Vender", fila["Gold"], fila["Gold_ma20"], fecha)
    time.sleep(1)

productor.flush()
print("Ya no quedan mensajes por enviar.")