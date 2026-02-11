from confluent_kafka import Consumer
import json

# Configuracion del consumidor
config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo-consumidor-final',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(config)

# Este topico lo crea KSQL en mayusculas
topic_kafka = 'PEDIDOS_CAROS'
consumer.subscribe([topic_kafka])

print(f"Esperando pedidos caros del topico '{topic_kafka}'...")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print(f"Error al recibir mensaje: {msg.error()}")
            continue

        # KSQL pone los campos en mayusculas
        datos = json.loads(msg.value().decode('utf-8'))

        print(f"PEDIDO CARO -> {datos['PEDIDO_ID']} | "
              f"{datos['RESTAURANTE']} | "
              f"{datos['PLATO']} | "
              f"Total: {datos['TOTAL']} EUR | "
              f"Cliente: {datos['CLIENTE']}")

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")

finally:
    consumer.close()
