import json
import time
import random
import uuid
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="127.0.0.1:9092", 
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def generate_sensor_data():
    return {
        "sensor_id": random.choice(["S1", "S2", "S3", "S4"]),
        "value": round(random.uniform(10, 50), 2),
        "temperature": round(random.uniform(20, 90), 2),
        "humidity": round(random.uniform(20, 90), 2),
        "status": random.choice(["OK", "WARN", "FAIL"]),
        "timestamp": time.time(),
        "uuid": str(uuid.uuid4())
    }

print("Iniciando envío de datos al topic: fake_data...")

try:
    while True:
        data = generate_sensor_data()
        
        # CAMBIO AQUÍ: El primer parámetro es el nombre del TOPIC
        producer.send("fake_data", data)
        
        print(f"Enviado a 'fake_data': {data['sensor_id']} | Temp: {data['temperature']}°C")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDeteniendo el productor...")
finally:
    producer.flush() # Asegura que todos los mensajes se envíen antes de cerrar
    producer.close()