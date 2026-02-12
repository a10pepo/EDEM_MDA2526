from confluent_kafka import Producer
import json
import time
import random

config = {'bootstrap.servers': 'localhost:9092', 'client.id': 'src-producer'}
producer = Producer(config)
topic_1 = 'raw_transactions'

users = ['Alice', 'Bob', 'Charlie', 'David', 'Eva']
statuses = ['Success', 'Failed', 'Cancelled', 'Success', 'Success'] 

print("Iniciando simulador de transacciones...")

try:
    i = 1
    while True:
        data = {
            'id': f'TX-{1000+i}',
            'user': random.choice(users),
            'card': f'{random.randint(4000,4999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}',
            'amount': round(random.uniform(50, 1000), 2), # Gastos entre 50 y 1000
            'status': random.choice(statuses)
        }
        
        producer.produce(topic_1, value=json.dumps(data).encode('utf-8'))
        print(f"Enviado RAW: {data['amount']} ({data['status']})")
        
        producer.flush()
        time.sleep(1) # Una venta cada segundo
        i += 1
except KeyboardInterrupt:
    print("Stop.")