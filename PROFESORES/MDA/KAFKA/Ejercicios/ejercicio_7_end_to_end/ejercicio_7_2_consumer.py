from confluent_kafka import Consumer
import time
import json

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': f'grupo_ejercicio_2_{int(time.time())}',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['transferencias'])


print("\n--- Consumiendo todas las transferencias ---")
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        #print('no transfers found')
        continue
    data = json.loads(msg.value().decode('utf-8'))
    print(data)

consumer.close()