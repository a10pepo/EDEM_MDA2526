import time
import json
import random
from confluent_kafka import Producer
from datetime import datetime

# --- CONFIGURACIÓN ---
TOPIC_NAME = 'raw-transactions'
conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'fintech-producer-source'
}

producer = Producer(conf)

# --- DATOS MOCK ---
CURRENCIES = ['USD', 'GBP', 'EUR'] 
STATUSES = ['SUCCESS', 'SUCCESS', 'SUCCESS', 'SUCCESS', 'FAILED'] 

def delivery_report(err, msg):
    if err is not None:
        print(f'❌ Error: {err}')
    else:
        # Esto imprime lo que envías. Fíjate que ahora usa transaction_id
        print(f'✅ Enviado: {msg.value().decode("utf-8")}')

def generate_transaction():
    return {
        "transaction_id": f"tx_{random.randint(10000, 99999)}", # EL CAMPO IMPORTANTE
        "user_id": f"user_{random.randint(1, 10)}",             # IMPORTANTE PARA KSQL
        "amount": round(random.uniform(50.0, 5000.0), 2),
        "currency": random.choice(CURRENCIES),
        "status": random.choice(STATUSES),
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }

print("🚀 Iniciando Producer PRO... (Ctrl+C para parar)")

while True:
    data = generate_transaction()
    producer.produce(TOPIC_NAME, key=data['user_id'], value=json.dumps(data), callback=delivery_report)
    producer.flush()
    time.sleep(2)