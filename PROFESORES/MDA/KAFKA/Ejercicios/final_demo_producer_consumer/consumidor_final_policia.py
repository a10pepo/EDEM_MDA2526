from confluent_kafka import Consumer
import time
import json
#*********Remeber to install this library with =>  pip install colorama  *!!!!!!!*********************
from colorama import Fore, Style, init

init(autoreset=True)

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': f'grupo_policia',
    'auto.offset.reset': 'latest'
}
consumer = Consumer(conf)
consumer.subscribe(['alertas_confirmadas'])

print(Fore.CYAN + "🦹  Policía escuchando alertas...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(Fore.RED + f"Error: {msg.error()}")
            continue

        datos = json.loads(msg.value().decode('utf-8'))
        if datos.get("alerta_tipo") == "robo":
            # Fecha y hora actual
            momento = time.strftime("%Y-%m-%d %H:%M:%S")
             # Mensaje detallado
            print(Fore.RED + Style.BRIGHT +
                    f"🦹 [{momento}] Intrusión detectada. Enviando patrulla de policía a {datos.get('nombre')} "
                    f"(Ubicación ID: {datos.get('ubicacion_id')})")

except KeyboardInterrupt:
    print(Fore.CYAN + "Policía detenido.")
finally:
    consumer.close()