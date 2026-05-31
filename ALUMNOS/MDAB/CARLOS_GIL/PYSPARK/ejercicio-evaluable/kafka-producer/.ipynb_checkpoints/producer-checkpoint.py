import json
import time
import random
import uuid
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
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

while True:
    data = generate_sensor_data()
    producer.send("sensores", data)
    print("Enviado:", data)
    time.sleep(1)
