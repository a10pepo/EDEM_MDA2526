import time
from json import dumps
from confluent_kafka import Producer
import random

config = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'python-producer'
}

producer = Producer(config)

topic_kafka = 'pedidos'

restaurantes = ['Telepizza', 'Dominos', 'BurgerKing', 'SushiTime', 'TacoBell']
clientes = ['Jorge', 'Maria', 'Lucia', 'Carlos', 'Laura', 'Pedro']

pedido_id = 0
while True:
    time.sleep(1)
    distancia = f'{random.randint(1, 30)}'
    pedido = {
        'pedido_id': str(pedido_id),
        'restaurante': random.choice(restaurantes),
        'cliente': random.choice(clientes),
        'distancia': distancia
    }
    pedido_json = dumps(pedido)
    pedido_bytes = pedido_json.encode('utf-8')
    producer.produce(topic = topic_kafka, value = pedido_bytes)
    producer.flush()
    pedido_id += 1
    print(pedido_json)
