import json
from kafka import KafkaConsumer, KafkaProducer

# 1. Configuramos el Consumer (el que lee del primer topic)
consumer = KafkaConsumer(
    'compras_raw',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest' # Lee desde el principio si es la primera vez
)

# 2. Configuramos el Producer (el que envía al segundo topic)
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Esperando ventas para procesar.")

try:
    for message in consumer:
        venta = message.value
        
        # Añadimos un mensaje 
        venta['notificacion'] = f"¡Enhorabuena {venta['cliente']}! Tu {venta['modelo']} ya está registrado."
    
        
        # Enviamos el JSON al nuevo topic
        producer.send('compras_enriquecidas', value=venta)
        
        print(f"✅ Venta de {venta['cliente']} procesada y reenviada.")

except KeyboardInterrupt:
    print("\nDeteniendo el transformador...")
finally:
    producer.close()