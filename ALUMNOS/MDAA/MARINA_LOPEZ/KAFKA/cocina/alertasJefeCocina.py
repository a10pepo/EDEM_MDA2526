from confluent_kafka import Consumer, Producer
import json
from colorama import Fore, Style, init
import time


# Inicializa colorama con autoreset
init(autoreset=True)

conf_consumer = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'jefe_cocina',
    'auto.offset.reset': 'latest'
}
consumer = Consumer(conf_consumer)
consumer.subscribe(['pedidos_cocina'])

conf_producer = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf_producer)

print(f"{Fore.MAGENTA}{Style.BRIGHT}👨‍🍳 JEFE DE COCINA: Organizando la sala...")


try:
    while True:
        msg = consumer.poll(1.0)  # Espera hasta 1 segundo por un mensaje
        if msg is None:
            # No hay mensaje disponible en este momento, seguimos esperando
            continue

        if msg.error():
            # Si hay un error en el mensaje, lo mostramos
            print(f"Error al recibir pedido: {msg.error()}")
            continue
        pedido = json.loads(msg.value().decode('utf-8'))
        tipo_comida = pedido['plato']['tipo']  
        nombre_plato = pedido['plato']['nombre']
        mesa = pedido['mesa']

        topic_destino = ""
        if tipo_comida == "pizza":
            topic_destino = "pedidos_pizza"
            print(f"{Fore.BLUE}🚨 pedido de {nombre_plato} (Mesa{mesa} -> {Fore.GREEN}Derivado a Pizzeros")

        elif tipo_comida == "pasta":
            topic_destino = "pedidos_pasta"
            print(f"{Fore.BLUE}🚨 pedido de {nombre_plato} (Mesa {mesa}) -> {Fore.YELLOW}Derivado a Pasteros")
        
        pedido_str = json.dumps(pedido, ensure_ascii=False)
        pedido_bytes = pedido_str.encode('utf-8')
        producer.produce(topic_destino, value = pedido_bytes)


except KeyboardInterrupt:
    print((f"{Fore.RED}Jefe de cocina cierra el turno (por el usuario)."))
finally:
    consumer.close()
