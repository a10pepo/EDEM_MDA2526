from confluent_kafka import Producer, Consumer
import json
import string
import time
import random
from colorama import Fore, Style, init

# Inicializa colorama con autoreset
init(autoreset=True)

# Configuración del productor Kafka
conf = {
    'bootstrap.servers': 'localhost:9092'  # Ajusta según tu broker
}
producer = Producer(conf)

conf_consumer = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': f'grupo_alertas_{int(time.time())}',
    'auto.offset.reset': 'latest'
}
consumer = Consumer(conf_consumer)
consumer.subscribe(['encargos_coches'])
consumer.subscribe(['encargos_piezas'])



def encargar_piezas(mensaje, piezas):
    producer.produce(
        topic='encargo_piezas',
        value=json.dumps(mensaje, ensure_ascii=False).encode('utf-8')
    )
    producer.flush()
    print(Fore.YELLOW + f"🔄 Encargo de {piezas} enviado al proveedor. Aviso enviado al topic 'encargo_piezas'")

def reparacion_finalizada(mensaje):
    producer.produce(
        topic='encargos_finalizados',
        value=json.dumps(mensaje,ensure_ascii=False).encode('utf-8')
    )
    producer.flush()
    print(Fore.GREEN + f"✅ Reparación del vehiculo {mensaje["matricula"]} finalizada. Aviso enviado al topic 'encargos_finalizados'")

