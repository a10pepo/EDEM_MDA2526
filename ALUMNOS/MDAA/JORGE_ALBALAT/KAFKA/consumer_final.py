from json import loads
from confluent_kafka import Consumer
config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo_soporte',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(config)
topic_kafka = 'PEDIDOS_LENTOS'
consumer.subscribe([topic_kafka]) 

while True:
    msg = consumer.poll(1)
    if msg is None: 
        continue
    elif msg.error(): 
        continue

    
    datos = msg.value().decode('utf-8')
    datos = loads(datos)
    
    print(f"\n⚠️  RETRASO DETECTADO")
    print(f"   ID:          {datos.get('ID')}")
    print(f"   Cliente:     {datos.get('CLIENTE')}")
    print(f"   Restaurante: {datos.get('RESTAURANTE')}")
    print(f"   Tiempo Est:  {datos.get('TIEMPO')} minutos")
    print("--------------------------------")