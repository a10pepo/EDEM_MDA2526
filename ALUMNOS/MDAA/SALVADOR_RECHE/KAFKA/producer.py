from confluent_kafka import Producer
import json
import time
import random
from colorama import Fore, init

init(autoreset=True)

conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

print(Fore.CYAN + "🎣 Barco faenando... Esperando capturas...")

try:
    while True:
        time.sleep(random.uniform(0.5, 2)) # Pescan rápido
        
        # Generamos datos
        es_tiburon = random.choice([True, False])
        
        if es_tiburon:
            especie = "Tiburón"
            icono = "🦈"
            peso = random.randint(40, 150) # Tiburones variados
        else:
            especie = "Atún"
            icono = "🐟"
            peso = random.randint(30, 90) # Atunes (unos para lata, otros para filete)

        mensaje = {
            "id_captura": f"CAP-{random.randint(1000, 9999)}",
            "especie": especie,
            "icono": icono,
            "peso_kg": peso,
            "timestamp": time.strftime("%H:%M:%S")
        }

        print(f"🎣 Entrada: {icono} {especie} de {peso}kg")
        
        # Enviamos al primer topic
        producer.produce(topic='ingesta_pesca', value=json.dumps(mensaje).encode('utf-8'))
        producer.flush()

except KeyboardInterrupt:
    print("Barco regresando a puerto.")