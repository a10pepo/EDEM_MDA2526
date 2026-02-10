# IMPORTACIÓN DE LIBRERÍAS
from confluent_kafka import Consumer    # Librería para consumir mensajes de Apache Kafka
from flask import config, json


# CONFIGURACIÓN DEL CONSUMIDOR
config = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker Kafka (como la IP de un servicio web)
    'group.id': 'final_squad-group',           # Identificador del grupo de consumidores
    'auto.offset.reset': 'earliest'         # Leer desde el principio si no hay posición guardada
}


# Creamos el consumidor con la configuración anterior
consumer = Consumer(config)

# Nos suscribimos al tópico que queremos leer
input_topic_ksql = 'SPANISH_FINAL_SQUAD'

consumer.subscribe([input_topic_ksql])
print(f"Leyendo la lista definitiva del topic '{input_topic_ksql}'...")

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

        # Procesamiento de datos
        try:
            data = json.loads(msg.value().decode('utf-8'))  # Convertimos el mensaje de bytes a JSON

            name = data.get('name') or data.get('NAME')
            position = data.get('position') or data.get('POSITION')
            rating = data.get('rating') or data.get('RATING')
            age_range = data.get('age_range') or data.get('AGE_RANGE')
            team = data.get('team') or data.get('TEAM')

            print(f"Jugador en la lista definitiva': {name} ({position}, {rating}, {age_range}, {team})")

        except Exception as e:
            print(f"Error al procesar mensaje: {e}")

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")

finally:
    # Cerramos el consumidor para liberar recursos
    consumer.close()