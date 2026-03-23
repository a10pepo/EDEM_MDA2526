from confluent_kafka import Consumer, Producer

# Configuración del consumer (lee de Kafka)
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'consumidor-natacion',
    'auto.offset.reset': 'earliest'
})

# Configuración del producer (escribe a otro topic)
producer = Producer({
    'bootstrap.servers': 'localhost:9092'
})

# Me suscribo al topic donde están todos los datos
consumer.subscribe(['datos_strava'])

print("Esperando datos de natación...")

while True:
    msg = consumer.poll(1.0)

    # Si no hay mensaje, seguimos esperando
    if msg is None:
        continue

    if msg.error():
        print("Error:", msg.error())
        continue

    # Decodifico el mensaje
    texto = msg.value().decode('utf-8')

    # Si el mensaje es de natación, lo mando a otro topic
    if 'Natación' in texto:
        producer.produce('natacion_procesada', value=texto.encode('utf-8'))
        producer.flush()
        print("Natación enviada al topic natacion_procesada")