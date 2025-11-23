
import datetime
import time
import random
from json import dumps


from confluent_kafka import Producer


config = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'python-producer'
}

producer = Producer(config)


topic_kafka = 'pataton'

inverterDict=dict()

while True:
    inverterID=random.randint(1,100)

    totalConsumption=random.randint(1,100)
    totalGeneration=random.randint(1,100)

    if inverterID not in inverterDict:
        inverterDict[inverterID] = {}
        inverterDict[inverterID]["totalConsumption"]=1
        inverterDict[inverterID]["totalGeneration"]=1


    inverterDict[inverterID]["id"]=inverterID
    inverterDict[inverterID]["totalConsumption"]+=totalConsumption
    inverterDict[inverterID]["totalGeneration"]+=totalGeneration
    inverterDict[inverterID]["timestamp"]=datetime.datetime.timestamp(datetime.datetime.now())


    data_str = dumps( inverterDict[inverterID], ensure_ascii=False)

    data_bytes = data_str.encode('utf-8')
    
    producer.produce(topic=topic_kafka, value=data_bytes)
        

    # Mostramos en pantalla lo que estamos enviando.
    print(f"Enviando datos: {inverterDict} al tópico {topic_kafka}")

    # Pausa de 1 segundo entre mensajes para simular un flujo en tiempo real.
    time.sleep(1)
pending = producer.flush()

if pending != 0:
    print(f"{pending} mensajes no se pudieron entregar.")