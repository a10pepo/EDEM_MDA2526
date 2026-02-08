import json
from kafka import KafkaConsumer, KafkaProducer


CONSUMER_TOPIC = 'raw-transactions'
PRODUCER_TOPIC = 'clean-transactions'

consumer = KafkaConsumer(
    CONSUMER_TOPIC,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("Iniciando procesador ETL (Filtrado y Transformación)...")

for message in consumer:
    data = message.value
    
    # 1.Eliminar tarjeta de crédito
    if "tarjeta_credito" in data:
        del data["tarjeta_credito"]
    
    # 2.Convertir categoría a Mayúsculas
    data["categoria"] = data["categoria"].upper()
    
    # 3.Añadir marca de procesado
    data["procesado_por"] = "ETL_Python_v1"
    
    # Enviar al siguiente topic
    producer.send(PRODUCER_TOPIC, value=data)
    print(f"Procesado y reenviado: {data}")