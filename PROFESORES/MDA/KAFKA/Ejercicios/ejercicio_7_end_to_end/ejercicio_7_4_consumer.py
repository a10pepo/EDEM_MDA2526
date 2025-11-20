from confluent_kafka import Consumer
import json

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': f'grupo_ejercicio_4_{int(time.time())}',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['transferencias'])

totales = {}
print("\n--- Suma de montos por país de origen ---")
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    data = json.loads(msg.value().decode('utf-8'))

    pais = data['pais_origen']
    totales[pais] = totales.get(pais, 0) + data['monto']
    print('***UPDATE START****')
    for pais, total in totales.items():
        print(f"{pais}: {total}")

    print('***UPDATE END****\n\n')

consumer.close()
