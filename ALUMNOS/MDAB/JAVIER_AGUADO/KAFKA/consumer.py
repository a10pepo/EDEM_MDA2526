import time
import json
from datetime import datetime
from confluent_kafka import Consumer
from confluent_kafka import Producer

# Consumer
topic_kafka = 'temperatura_Valencia'
config_consumer = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker Kafka (como la IP de un servicio web)
    'group.id': 'grupo-consumidor'         # Identificador del grupo de consumidores
}
consumer = Consumer(config_consumer)
consumer.subscribe([topic_kafka])

# Producer 2
topic_kafka_producer = 'temperatura_Valencia_procesada'
config_producer = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del servidor Kafka (cambiar si está en otra máquina)
    'client.id': 'productor-python2'  # Identificador único para este productor
}
productor = Producer(config_producer)

hist_temp = []
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error al recibir mensaje: {msg.error()}")
            continue

        # Conversión y publicación dato en nuevo topico
        msg_str = msg.value().decode('utf-8')
        msg_dict  = json.loads(msg_str)

        # Guardar para acumular histórico y analizar
        hist_temp.append(msg_dict)

        suma = 0
        for datos in hist_temp:
            if datos['fecha'] == datetime.today().strftime("%Y-%m-%d"):
                suma += round(datos['temperatura'], 2)
        media = round(suma / len(hist_temp), 2)

        temp_analizada = 'frio de cojones'
        if media > 0:
            temp_analizada = 'mucho frio'
        if media >= 10:
            temp_analizada = 'frio'
        if media >= 18:
            temp_analizada = 'buena temperatura'
        if media >= 24:
            temp_analizada = 'calor'
        if media >= 30:
            temp_analizada = 'mucho calor'

        # Generar dato para nueva producción
        result = f"Con temperatura media {media}º en Valencia hace {temp_analizada}."
        print(result)

        # Publicar nuevo dato
        result_str = json.dumps(result, ensure_ascii=False)
        result_bytes = result_str.encode('utf-8')
        productor.produce(topic=topic_kafka_producer, value=result_bytes)

        time.sleep(10)
except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
finally:
    consumer.close()    
    productor.flush()