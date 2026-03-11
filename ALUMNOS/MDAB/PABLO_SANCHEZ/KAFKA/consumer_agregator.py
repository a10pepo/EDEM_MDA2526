from kafka import KafkaConsumer, KafkaProducer
import json
from collections import defaultdict

consumer = KafkaConsumer(
    'processed-orders',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='aggregator-group'
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

stats = defaultdict(lambda: {'total_orders': 0, 'total_revenue': 0.0})

print(" Agregador iniciado - Calculando estadísticas...")

for message in consumer:
    order = message.value
    status = order['status']
    
    stats[status]['total_orders'] += 1
    stats[status]['total_revenue'] += order['price']
    
    avg_value = stats[status]['total_revenue'] / stats[status]['total_orders']
    
    stat_message = {
        'STATUS': status,
        'TOTAL_ORDERS': stats[status]['total_orders'],
        'TOTAL_REVENUE': round(stats[status]['total_revenue'], 2),
        'AVG_ORDER_VALUE': round(avg_value, 2)
    }
    
    producer.send('orders-stats', value=stat_message)
    
    print(f" Stats {status}: {stats[status]['total_orders']} pedidos | ${stats[status]['total_revenue']:.2f}")

    