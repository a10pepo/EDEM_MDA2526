import time
import requests
from json import dumps
from confluent_kafka import Producer  # Librería para producir mensajes en Apache Kafka

topic_kafka = 'temperatura_Valencia'
TOKEN = "cd70607350ebb03422d5f512659edb25e8d38f32"
URL = f"https://api.waqi.info/feed/valencia/?token={TOKEN}"

configuracion = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del servidor Kafka (cambiar si está en otra máquina)
    'client.id': 'productor-python1'  # Identificador único para este productor
}
productor = Producer(configuracion)

response = requests.get(URL)
data = response.json()
if data["status"] == "ok":
    try:
        while True:
            temperatura_actual = data["data"]["iaqi"]["t"]["v"]
            fecha = data["data"]["time"]["s"]
            msg = {
                "ciudad": "Valencia",
                "fecha": fecha[:10],
                "hora": fecha[11:],
                "temperatura": temperatura_actual
            }
            msg_str = dumps(msg, ensure_ascii=False)
            msg_bytes = msg_str.encode('utf-8')
            productor.produce(topic=topic_kafka, value=msg_bytes)
            
            print(f"Temperatura actual: {temperatura_actual} °C")
            print(f"Fecha/hora medición: {fecha}")

            # producir dato cada 10 segundos
            time.sleep(10)
    except KeyboardInterrupt:
        print('Programa finalizado por usuario.')
else:
    print("Error al obtener datos")

# Esperamos a que todos los mensajes pendientes se envíen antes de terminar
productor.flush()