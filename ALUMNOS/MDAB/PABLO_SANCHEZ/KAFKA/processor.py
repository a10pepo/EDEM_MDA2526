from kafka import KafkaConsumer, KafkaProducer
import json

consumer = KafkaConsumer(
    'raw-orders',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='order-processor-group'
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print(" Consumer Procesador iniciado - Procesando pedidos...")

for message in consumer:
    order = message.value
    
    # TRANSFORMACIÓN: Agregar prioridad
    if order['price'] > 800:
        order['priority'] = 'HIGH'
    elif order['price'] > 300:
        order['priority'] = 'MEDIUM'
    else:
        order['priority'] = 'LOW'
    
    # Categorizar por producto
    if 'Laptop' in order['product'] or 'iPhone' in order['product']:
        order['category'] = 'Electronics'
    elif 'TV' in order['product']:
        order['category'] = 'Home Appliances'
    else:
        order['category'] = 'Gaming'
    
    producer.send('processed-orders', value=order)
    
    print(f"  Procesado: {order['order_id']} | Prioridad: {order['priority']} | Categoría: {order['category']}")
