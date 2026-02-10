import json
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

canciones = ["SONG_01", "SONG_02", "SONG_03", "SONG_04", "SONG_05"]
dispositivos = ["iPhone", "Android", "Web Player", "Smart TV"]

print("Enviando flujo de datos avanzado con telemetría...")

try:
    while True:
        # Simulamos una IP de un 'Bot' 
        es_bot = random.random() < 0.1  # 10% de probabilidad de ser un bot
        ip_cliente = "192.168.1.50" if es_bot else f"10.0.0.{random.randint(1, 254)}"
        
        mensaje = {
            "track_id": random.choice(canciones),
            "action": "play",
            "duracion_seg": random.randint(1, 200),
            "pais": random.choice(["ES", "MX", "AR", "US"]),
            "ip": ip_cliente,
            "dispositivo": random.choice(dispositivos),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        
        producer.send('music_raw_events', value=mensaje)
        print(f"Evento: {mensaje['track_id']} | IP: {ip_cliente} | Dev: {mensaje['dispositivo']}")
        
        # Si es bot, envía ráfagas rápidas
        time.sleep(0.1 if es_bot else 0.8)

except KeyboardInterrupt:
    print("Productor finalizado.")