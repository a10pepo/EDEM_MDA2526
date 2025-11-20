from confluent_kafka import Consumer
import json

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': f'grupo_ejercicio_3_{int(time.time())}',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['transferencias'])

print("\n--- Filtrando por Islas Caimán o Singapur ---")
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    data = json.loads(msg.value().decode('utf-8'))
    if data['pais_origen'] in ['Islas Caimán', 'Singapur'] or data['pais_destino'] in ['Islas Caimán', 'Singapur']:
        print(data)

consumer.close()