import time
from confluent_kafka import Producer
import os

config = {'bootstrap.servers': 'localhost:9092', 'client.id': 'sensor-producer'}
producer = Producer(config)
topic_kafka = 'lecturas-temperatura'

file_path = os.path.join(os.path.dirname(__file__), 'sensor_temperatura.txt')

with open(file_path, encoding="utf8") as file:
    file_lines = file.readlines()

print("Iniciando monitor de temperatura...")

for line in file_lines:
    time.sleep(2)
    print(f"Sensor enviando: {line.strip()}")
    producer.produce(topic=topic_kafka, value=line.strip().encode('utf-8'))
    producer.poll(0) 

producer.flush()