import json
from kafka import KafkaConsumer, KafkaProducer

INPUT_TOPIC = 'pedidos_raw'
OUTPUT_TOPIC = 'pedidos_vip'


consumer = KafkaConsumer(
    INPUT_TOPIC,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest', 
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print(f"--> Procesador iniciado. Leyendo de {INPUT_TOPIC} filtrando > 100")

for message in consumer:
    order = message.value
    
    if order['amount'] > 100:
        order['status'] = 'VIP_CUSTOMER'
        
        producer.send(OUTPUT_TOPIC, value=order)
        print(f"[PROCESADO VIP] Orden {order['order_id']} de {order['amount']} -> Enviado a {OUTPUT_TOPIC}")
    else:
        print(f"[Ignorado] Orden {order['order_id']} es menor a 100 ({order['amount']})")