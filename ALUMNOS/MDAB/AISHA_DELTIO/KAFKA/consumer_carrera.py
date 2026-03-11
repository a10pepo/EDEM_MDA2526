from confluent_kafka import Consumer, Producer

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'consumidor-carrera',
    'auto.offset.reset': 'earliest'
})

producer = Producer({
    'bootstrap.servers': 'localhost:9092'
})

consumer.subscribe(['datos_strava'])

print("Esperando datos de carrera...")

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        print("Error:", msg.error())
        continue

    texto = msg.value().decode('utf-8')

    if 'Carrera' in texto:
        producer.produce('carrera_procesada', value=texto.encode('utf-8'))
        producer.flush()
        print("Carrera enviada al topic carrera_procesada")