from confluent_kafka import Consumer, Producer
import json

# Configuración
conf_consumer = {
    'bootstrap.servers': 'localhost:9092', # Dirección del broker Kafka (como la IP de un servicio web)
    'group.id': 'cleaner-group', # Identificador del grupo de consumidores
    'auto.offset.reset': 'earliest' # Leer desde el principio si no hay posición guardada
}
conf_producer = {'bootstrap.servers': 'localhost:9092', 'client.id': 'cleaner-prod'}

consumer = Consumer(conf_consumer)
producer = Producer(conf_producer)

topic_in = 'raw_transactions'
topic_out = 'clean_transactions'

consumer.subscribe([topic_in])

print("Iniciando proceso de limpieza...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        if msg.error(): continue

        # 1. Deserializar
        data = json.loads(msg.value().decode('utf-8'))

        # LOGICA DE NEGOCIO (Transformación)
        
        # A. Filtrar: Si no es 'Success', lo descartamos
        if data['status'] != 'Success':
            print(f"Descartada TX fallida: {data['id']}")
            continue

        # B. Anonimizar: Enmascarar tarjeta
        original_card = data['card']
        data['card'] = "****-****-****-" + original_card[-4:]

        # 2. Enviar al siguiente Tópico
        producer.produce(topic_out, value=json.dumps(data).encode('utf-8'))
        producer.flush()
        
        print(f"Procesada y enviada a '{topic_out}': {data['id']} - ${data['amount']}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()