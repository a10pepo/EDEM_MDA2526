from confluent_kafka import Consumer, Producer
import json

# Configuracion del consumidor
conf_consumer = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo-procesador',
    'auto.offset.reset': 'earliest'
}

# Configuracion del productor para reenviar los datos procesados
conf_producer = {
    'bootstrap.servers': 'localhost:9092'
}

consumer = Consumer(conf_consumer)
producer = Producer(conf_producer)

# Topicos de entrada y salida
topic_entrada = 'pedidos'
topic_salida = 'pedidos_procesados'

consumer.subscribe([topic_entrada])

print(f"Esperando mensajes del topico '{topic_entrada}'...")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print(f"Error al recibir mensaje: {msg.error()}")
            continue

        # Deserializamos el mensaje de bytes a diccionario
        datos = json.loads(msg.value().decode('utf-8'))

        # Filtrado: solo procesamos pedidos confirmados
        if datos['estado'] != 'confirmado':
            print(f"  DESCARTADO {datos['pedido_id']} -> estado: {datos['estado']}")
            continue

        # Transformacion: calculamos el total
        total = datos['cantidad'] * datos['precio']

        # Creamos el mensaje procesado con el campo total nuevo
        datos_procesados = {
            'pedido_id': datos['pedido_id'],
            'restaurante': datos['restaurante'],
            'plato': datos['plato'],
            'cantidad': datos['cantidad'],
            'precio': datos['precio'],
            'total': round(total, 2),
            'cliente': datos['cliente'],
            'metodo_pago': datos['metodo_pago']
        }

        print(f"Procesado: {datos_procesados['pedido_id']} | {datos_procesados['plato']} | Total: {datos_procesados['total']} EUR")

        # Enviamos al topico de salida
        producer.produce(
            topic=topic_salida,
            value=json.dumps(datos_procesados, ensure_ascii=False).encode('utf-8')
        )
        producer.flush()

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")

finally:
    consumer.close()
