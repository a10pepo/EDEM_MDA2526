from confluent_kafka import Consumer, Producer
from json import loads, dumps
config = {
    'bootstrap.servers': 'localhost:9092',  
    'group.id': 'grupo-consumidor',         
    'auto.offset.reset': 'earliest'
}
config2 = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'python-producer2',
}
producer = Producer(config)
consumer = Consumer(config)

topic_kafka = 'pedidos'
topic_kafka2 = 'pedidos_tiempo'
consumer.subscribe([topic_kafka])

velocidad = 4 # velocidad del repartidor min/km

while True:
    msg = consumer.poll(1)
    if msg is None:
        continue
    elif msg.error():
        continue
    mensaje = msg.value().decode('utf-8')
    pedido = loads(mensaje)
        
    distancia = int(pedido['distancia'])
    tiempo = (distancia * velocidad)
        
    pedido_procesado = {
        "id": pedido['pedido_id'],
        "cliente": pedido['cliente'],
        "restaurante": pedido['restaurante'],
        "tiempo": str(tiempo)
    }
    pedido_json = dumps(pedido_procesado)
    pedido_bytes = pedido_json.encode('utf-8')
    print(pedido_json)
    producer.produce(topic = topic_kafka2, value = pedido_bytes)
    producer.flush()