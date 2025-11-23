from confluent_kafka import Consumer
import json
config = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker Kafka (como la IP de un servicio web)
    'group.id': 'grupo-consumidor',         # Identificador del grupo de consumidores
    'auto.offset.reset': 'earliest'         # Leer desde el principio si no hay posición guardada
}

consumer = Consumer(config)

topic_kafka = 'informacion_inversores'
consumer.subscribe([topic_kafka])

print(f"Esperando mensajes del tópico '{topic_kafka}'...")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print(f"Error al recibir mensaje: {msg.error()}")
            continue
        value=msg.value().decode('utf-8')
        inverterMessage=json.loads(value)
        print(f"Mensaje recibido: {inverterMessage}. Tipo: {type(inverterMessage)}")
        

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")

finally:
    consumer.close()