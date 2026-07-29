from kafka import KafkaProducer
import json
import time
import random

# Configuración del Productor
# Se conecta al puerto 9092 (el que expusiste en docker-compose para localhost)
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

TOPIC_NAME = 'traffic_raw'
SENSORS = ['S-101', 'S-102', 'S-103', 'S-104']

print(f"🚗 Iniciando simulador de tráfico. Enviando datos a '{TOPIC_NAME}'...")
print("Presiona Ctrl+C para detener.")

try:
    while True:
        # Generamos datos aleatorios de tráfico
        current_speed = random.randint(80, 160) # Velocidad entre 80 y 160 km/h
        
        data = {
            "sensor_id": random.choice(SENSORS),
            "vehicle_plate": f"ABC-{random.randint(1000, 9999)}",
            "speed": current_speed,
            "lane": random.randint(1, 3),
            "timestamp": time.time()
        }
        
        # Enviar el mensaje a Kafka
        producer.send(TOPIC_NAME, value=data)
        
        # Imprimir en consola para que veas qué está pasando
        print(f"Enviado: {data}")
        
        time.sleep(1) # Espera 1 segundo entre mensajes
except KeyboardInterrupt:
    print("\nDeteniendo productor...")
    producer.close()
    