from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'orders-stats',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='stats-viewer-group'
)

print(" Consumer Final - Mostrando estadísticas en tiempo real...\n")
print("="*80)

for message in consumer:
    stats = message.value
    
    print(f"\n🔔 ESTADÍSTICAS ACTUALIZADAS:")
    print(f"   Estado: {stats.get('STATUS', 'N/A')}")
    print(f"   Total Pedidos: {stats.get('TOTAL_ORDERS', 0)}")
    print(f"   Revenue Total: ${stats.get('TOTAL_REVENUE', 0):.2f}")
    print(f"   Valor Promedio: ${stats.get('AVG_ORDER_VALUE', 0):.2f}")
    print("="*80)
