
import datetime
import time
import random
from json import dumps
import os


from confluent_kafka import Producer

BASE_URL = os.getenv("SERVER_URL", "http://localhost:9092")

config = {
    'bootstrap.servers': BASE_URL,
    'client.id': 'python-producer'
}

producer = Producer(config)


topic_kafka = 'inverter_data'

inverterDict=dict()

while True:
    inverterID=random.randint(1,100)

    totalConsumption=random.randint(1,100)
    totalGeneration=random.randint(1,100)

    if inverterID not in inverterDict:
        inverterDict[inverterID] = {}
        inverterDict[inverterID]["totalConsumption"]=totalConsumption
    else:
        inverterDict[inverterID]["totalConsumption"]+=totalConsumption

    inverterDict[inverterID]["device_id"]=inverterID
    inverterDict[inverterID]["timestamp"]=datetime.datetime.timestamp(datetime.datetime.now())


    data_str = dumps( inverterDict[inverterID], ensure_ascii=False)

    data_bytes = data_str.encode('utf-8')
    
    producer.produce(topic=topic_kafka, value=data_bytes)
    producer.flush()

    # Mostramos en pantalla lo que estamos enviando.
    print(f"Enviando datos: {inverterDict[inverterID]} al tópico {topic_kafka}")

    # Pausa de 1 segundo entre mensajes para simular un flujo en tiempo real.
    # time.sleep(10)
