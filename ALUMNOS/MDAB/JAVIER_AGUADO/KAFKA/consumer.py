from confluent_kafka import Consumer
from confluent_kafka import Producer  # Librería para producir mensajes en Apache Kafka
import json

# Consumer
topic_kafka = 'temperatura_Valencia'
config_consumer = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker Kafka (como la IP de un servicio web)
    'group.id': 'grupo-consumidor'         # Identificador del grupo de consumidores
}
consumer = Consumer(config_consumer)
consumer.subscribe([topic_kafka])

# Producer
topic_kafka_producer = 'temperatura_Valencia_procesada'
config_producer = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del servidor Kafka (cambiar si está en otra máquina)
    'client.id': 'productor-python2'  # Identificador único para este productor
}
productor = Producer(config_producer)

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error al recibir mensaje: {msg.error()}")
            continue
        print(f"Mensaje recibido: {msg.value().decode('utf-8')}")

        # Conversión y publicación dato en nuevo topico
        msg_str = msg.value().decode('utf-8')
        msg_dict  = json.loads(msg_str)
        print(msg_dict)
        temperatura = float(msg_dict['temperatura'])
        result = 'Frio de cojones'
        if temperatura > 0:
            result = 'Mucho frio'
        if temperatura >= 10:
            result = 'Frio'
        if temperatura >= 18:
            result = 'Buena'
        if temperatura >= 24:
            result = 'Calor'
        if temperatura >= 30:
            result = 'Mucho calor'
        result_str = json.dumps(result, ensure_ascii=False)
        result_bytes = result_str.encode('utf-8')
        productor.produce(topic=topic_kafka_producer, value=result_bytes)

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
finally:
    consumer.close()    
    productor.flush()