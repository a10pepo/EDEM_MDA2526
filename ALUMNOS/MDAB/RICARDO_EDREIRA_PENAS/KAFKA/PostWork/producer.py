import time
import os
from json import dumps, loads

# Importamos el Producer de confluent_kafka
# pip install confluent-kafka
from confluent_kafka import Producer

# bootstrap.servers: dirección del broker Kafka en localhost:9092
# client.id: identificador de este productor
config = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'python-producer'
}

# Creamos el productor con la configuración
producer = Producer(config)

# Usamos un tópico para enviar los pedidos de restaurantes
topic_kafka = 'pedidos'

# Construimos la ruta al archivo pedidos.txt
ruta_archivo = os.path.join(os.path.dirname(__file__), 'pedidos.txt')

# Abrimos el archivo con codificación UTF-8 para soportar acentos y ñ
with open(ruta_archivo, encoding="utf8") as archivo:
    lineas = archivo.readlines()

# Recorremos cada línea del archivo, cada una es un JSON con un pedido
for linea in lineas:
    linea = linea.strip()
    if not linea:
        continue

    # Parseamos el JSON para poder mostrar los datos por pantalla
    data = loads(linea)

    # Convertimos a cadena JSON y luego a bytes, parq que lo entienda Kafka
    data_str = dumps(data, ensure_ascii=False)
    data_bytes = data_str.encode('utf-8')

    # Enviamos el mensaje al tópico
    producer.produce(topic=topic_kafka, value=data_bytes)

    # Mostramos por pantalla lo que se esta enviando
    print(f"Enviando: {data['pedido_id']} | {data['restaurante']} | {data['plato']}")

    # Pausa entre mensajes para que parezca en tiempo real y no sobre cargar el sistema
    time.sleep(1)

# flush para que espere a que TODOS los mensajes pendientes se envíen
pending = producer.flush()
if pending != 0:
    print(f"{pending} mensajes no se pudieron entregar.")

print("Todos los pedidos han sido enviados correctamente.")
