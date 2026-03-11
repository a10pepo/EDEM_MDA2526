from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

customers = ["Juan Perez", "Maria Garcia", "Carlos Lopez", "Ana Martinez"]
products = ["Laptop Dell", "iPhone 14", "Samsung TV", "PlayStation 5", "Airpods"]
statuses = ["PENDING", "PROCESSING", "SHIPPED", "DELIVERED"]

print(" Iniciando Producer - Generando pedidos...")

order_id = 1000
try:
    while True:
        order = {
            "order_id": f"ORD-{order_id}",
            "customer": random.choice(customers),
            "product": random.choice(products),
            "quantity": random.randint(1, 5),
            "price": round(random.uniform(50, 1500), 2),
            "status": random.choice(statuses),
            "timestamp": datetime.now().isoformat()
        }
        
        producer.send('raw-orders', value=order)
        print(f"✅ Pedido enviado: {order['order_id']} - {order['product']} - ${order['price']}")
        
        order_id += 1
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\n Producer detenido")
    producer.close()

