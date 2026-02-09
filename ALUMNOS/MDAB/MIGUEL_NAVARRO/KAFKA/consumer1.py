from confluent_kafka import Consumer


# CONFIGURACIÓN DEL CONSUMIDOR
config = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker Kafka (como la IP de un servicio web)
    'group.id': 'consumer-group',           # Identificador del grupo de consumidores
    'auto.offset.reset': 'earliest'         # Leer desde el principio si no hay posición guardada
}

# Creamos el consumidor con la configuración anterior
consumer = Consumer(config)

# Nos suscribimos al tópico que queremos leer
topic_kafka = 'laliga_players'
consumer.subscribe([topic_kafka])

print(f"Esperando mensajes del tópico '{topic_kafka}'...")

try:
    while True:
        # Intenta obtener un mensaje durante 1 segundo.
        msg = consumer.poll(1.0)        

        if msg is None:
            # Si no hay mensaje disponible en este momento, seguimos esperando
            continue

        if msg.error():
            # Si hay un error en el mensaje, lo mostramos
            print(f"Error al recibir mensaje: {msg.error()}")
            continue

        # Si el mensaje es válido, mostramos su contenido
        print(f"Mensaje recibido: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")


finally:
    # Cerramos el consumidor para liberar recursos
    consumer.close()