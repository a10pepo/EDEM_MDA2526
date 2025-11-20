from confluent_kafka import Consumer
import json

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': f'grupo_ejercicio_5_{int(time.time())}',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['transferencias'])

print("\n--- Transferencias Completadas ---")
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        break
    data = json.loads(msg.value().decode('utf-8'))
    if data['estado'] == 'Completada':
        print(data)

consumer.close()