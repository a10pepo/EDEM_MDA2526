# Este script cumple la última parte: El gerente solo verá las Pizzas VIP que KSQL ha filtrado.
from confluent_kafka import Consumer
import json
from colorama import Fore, Style, init

init(autoreset=True)

# Configuración: Escucha el topic que CREÓ KSQL
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo_gerencia',
    'auto.offset.reset': 'latest'
}
consumer = Consumer(conf)
consumer.subscribe(['pizzas_vip_topic']) # Topic creado por KSQL

print(f"{Fore.MAGENTA}{Style.BRIGHT}👔 GERENTE: Supervisando servicio VIP...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: 
            continue
        if msg.error():
            print(f"Error al recibir pedido: {msg.error()}") 
            continue

        # KSQL a veces pone el mensaje en mayúsculas o cambia algo, pero es JSON
        pedido = json.loads(msg.value().decode('utf-8'))
        
        # Extraemos datos (KSQL mantiene la estructura)
        nombre_plato = pedido['PLATO']['NOMBRE'] # KSQL suele poner claves en mayúsculas
        mesa = pedido['MESA']
        cliente = pedido['TIPO_CLIENTE']

        print(f"{Fore.MAGENTA}🌟 ATENCIÓN: Cliente {cliente} en Mesa {mesa} comiendo {nombre_plato}")

except KeyboardInterrupt:
    print((f"{Fore.RED}Gerente termina el turno (por el usuario)."))
finally:
    consumer.close()