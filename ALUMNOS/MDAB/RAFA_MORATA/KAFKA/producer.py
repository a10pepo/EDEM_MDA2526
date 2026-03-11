import time
import json
import random
from kafka import KafkaProducer

# Configuración
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

TOPIC_NAME = 'raw-transactions'

print("Iniciando simulador de ventas...")

try:
    while True:
        # Generar datos aleatorios
        data = {
            "id_transaccion": random.randint(1000, 9999),
            "cliente": random.choice(["Rafa", "Carlos", "Pablo", "David"]),
            "tarjeta_credito": f"4500-{random.randint(1000,9999)}-{random.randint(1000,9999)}-9010", #dato privado simulado
            "categoria": random.choice(["electronica", "hogar", "ropa", "deportes"]),
            "monto": round(random.uniform(50.0, 500.0), 2)
        }
        
        # Enviar a Kafka
        producer.send(TOPIC_NAME, value=data)
        print(f"Enviado: {data}")
        time.sleep(2) # Espera 2 segundos antes de enviar la siguiente transacción
except KeyboardInterrupt:
    print("Deteniendo productor.")