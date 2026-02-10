# IMPORTACIÓN DE LIBRERÍAS
from confluent_kafka import Consumer    # Librería para consumir mensajes de Apache Kafka
from confluent_kafka import Producer    # Librería para producir mensajes en Apache Kafka
from flask import config, json


# CONFIGURACIONES DEL CONSUMIDOR Y PRODUCTOR
config_consumer = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker Kafka (como la IP de un servicio web)
    'group.id': 'players-consumer1-group',           # Identificador del grupo de consumidores
    'auto.offset.reset': 'earliest'         # Leer desde el principio si no hay posición guardada
}

config_producer2 = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'spanish-producer2'
}

# Creamos consumidor y producor con las configuraciones anteriores
consumer = Consumer(config_consumer)
producer = Producer(config_producer2)

# Nos suscribimos al tópico que queremos leer
input_topic = 'laliga_players'
output_topic = 'spanishPlayers'

POSITION_PARTITION = {
    'Goalkeeper': 0,
    'Defender': 1,
    'Midfielder': 2,
    'Forward': 3
}

consumer.subscribe([input_topic])
print(f"Buscando jugadores españoles seleccionables en '{input_topic}'...")

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
            if data.get('nation') != 'Spain':
                continue

            age = data.get('age')
            if age <= 23:
                data['age_range'] = 'Wonderkid'
            elif 23 < age <= 30:
                data['age_range'] = 'Prime'
            else:
                data['age_range'] = 'Veteran'

            position = data.get('position')
            partition_id = POSITION_PARTITION.get(position, 3)  # Si la posición no está en el diccionario, asignamos a delantero (partición 3: Forward)

            json_str = json.dumps(data)  # Convertimos el diccionario a una cadena JSON
            json_bytes = json_str.encode('utf-8')  # Convertimos el diccionario de vuelta a bytes para Kafka
            producer.produce(
                topic=output_topic,     # Enviamos el mensaje al topic de Kafka
                value=json_bytes,
                partition=partition_id  # A la partición correspondiente
            )

            print(f"Jugador seleccionable enviado a '{output_topic}': {data['name']} ({position}, {data['age_range']})")
            producer.flush()

        except Exception as e:
            print(f"Error al procesar mensaje: {e}")

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")

finally:
    # Cerramos el consumidor para liberar recursos
    consumer.close()