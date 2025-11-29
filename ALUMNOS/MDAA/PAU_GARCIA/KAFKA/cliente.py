from confluent_kafka import Producer, Consumer
import json
import string
import time
import random
from colorama import Fore, Style, init

# Inicializa colorama con autoreset
init(autoreset=True)

conf_consumer = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': f'grupo_alertas_{int(time.time())}',
    'auto.offset.reset': 'latest' 
}
consumer = Consumer(conf_consumer)
consumer.subscribe(['avisos_cliente'])

if __name__ == "__main__":
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(Fore.RED + f"Error en el mensaje: {msg.error()}")
                continue
            encargo = json.loads(msg.value().decode('utf-8'))
            print(Fore.MAGENTA + f"<✌️ Su coche con matrícula {encargo.get("matricula")} ya está listo para recoger")

    except Exception as e:
        print(Fore.CYAN + f"Gestor detenido: {e}")