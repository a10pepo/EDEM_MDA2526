import time
import json
import random
from kafka import KafkaProducer

# Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8') # Serializar a JSON
)

TOPIC_NAME = 'pedidos_raw'
CATEGORIES = ['electronics', 'books', 'clothing', 'home', 'garden']

print(f"--> Iniciando generador de pedidos hacia el topic: {TOPIC_NAME}")

try:
    while True:
        order_id = random.randint(10000, 99999)
        amount = round(random.uniform(10.0, 500.0), 2) # Precio entre 10 y 500
        category = random.choice(CATEGORIES)
        user_id = f"user_{random.randint(1, 50)}"
        
        data = {
            "order_id": order_id,
            "category": category,
            "amount": amount,
            "user_id": user_id
        }
        
        producer.send(TOPIC_NAME, value=data)
        print(f"[Enviado] ID: {order_id} | Cat: {category} | Total: {amount}")
        
        time.sleep(2)

except KeyboardInterrupt:
    print("Deteniendo el producer...")
    producer.close()