from confluent_kafka import Consumer

# ============================================
# CONFIGURACIÓN DEL CONSUMIDOR
# ============================================
config = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker Kafka (como la IP de un servicio web)
    'group.id': 'grupo-consumidor',         # Identificador del grupo de consumidores
    'auto.offset.reset': 'earliest'         # Leer desde el principio si no hay posición guardada
}

# Creamos el consumidor con la configuración anterior
consumer = Consumer(config)

# Nos suscribimos al tópico que queremos leer
topic_kafka = 'bank_transfers'
consumer.subscribe([topic_kafka])

print(f"Esperando mensajes del tópico '{topic_kafka}'...")


try:
    while True:         # bucle infinito. porque queremos que el consumidor siga leyendo mensajes mientras el programa esté activo.
        # ============================================
        # consumer.poll(1.0):
        #   Intenta obtener un mensaje durante 1 segundo.
        #   Si llega un mensaje en ese tiempo, lo devuelve.
        #   Si no llega nada, devuelve None.
        # ¿Por qué 1 segundo?
        #   - Es un buen equilibrio: no bloquea demasiado tiempo y no consume recursos en exceso.
        # ============================================
        msg = consumer.poll(1.0)

        if msg is None:
            # No hay mensaje disponible en este momento, seguimos esperando
            continue

        if msg.error():
            # Si hay un error en el mensaje, lo mostramos
            print(f"Error al recibir mensaje: {msg.error()}")
            continue

        # Si el mensaje es válido, mostramos su contenido
        # msg.value() devuelve los datos en bytes, por eso usamos decode('utf-8') para convertirlos a texto
        print(f"Mensaje recibido: {msg.value().decode('utf-8')}")


except KeyboardInterrupt:
    print("Programa detenido por el usuario.")


finally:
    consumer.close()