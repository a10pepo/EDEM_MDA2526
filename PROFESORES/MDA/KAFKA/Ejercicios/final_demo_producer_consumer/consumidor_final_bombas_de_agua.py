from confluent_kafka import Consumer
import json
import time
from colorama import Fore, Style, init

# Inicializa colorama
init(autoreset=True)

# Configuración del consumidor
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo_agua',  # Grupo único por ejecución
    'auto.offset.reset': 'latest'
}
consumer = Consumer(conf)
consumer.subscribe(['alertas_confirmadas'])

print(Fore.CYAN + "💧 Sistema de agua escuchando alertas...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(Fore.RED + f"Error: {msg.error()}")
            continue

        datos = json.loads(msg.value().decode('utf-8'))
        if datos.get("alerta_tipo") == "inundación":
            # Fecha y hora actual
            momento = time.strftime("%Y-%m-%d %H:%M:%S")
            # Mensaje detallado
            print(Fore.BLUE + Style.BRIGHT +
                  f"💧[{momento}] ALERTA DE INUNDACIÓN: Activando bombas de agua en {datos.get('nombre')} "
                  f"(Ubicación ID: {datos.get('ubicacion_id')})")
except KeyboardInterrupt:
    print(Fore.CYAN + "Sistema de agua detenido.")
finally:
    consumer.close()