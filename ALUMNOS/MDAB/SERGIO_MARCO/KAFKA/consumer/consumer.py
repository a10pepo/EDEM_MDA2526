# ============================================
# CONSUMER - Lee de inventory_raw, transforma
# y envia a inventory_enriched
# ============================================
# Si price > 50 -> category_value: "High"
# Si price <= 50 -> category_value: "Standard"
# Mantiene: id, title, price, stock

from json import loads, dumps
from confluent_kafka import Consumer, Producer

# ============================================
# Configuracion del consumidor
# ============================================
consumer_config = {
    'bootstrap.servers': 'kafka:29092',
    'group.id': 'grupo-consumidor',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)
topic_origen = 'inventory_raw'
consumer.subscribe([topic_origen])

# ============================================
# Configuracion del productor
# (para enviar a inventory_enriched)
# ============================================
producer_config = {
    'bootstrap.servers': 'kafka:29092',
    'client.id': 'enrichment-producer'
}

producer = Producer(producer_config)
topic_destino = 'inventory_enriched'

# ============================================
# Bucle principal
# ============================================
print(f"Esperando mensajes del topic '{topic_origen}'...")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print(f"Error al recibir mensaje: {msg.error()}")
            continue

        # Decodificamos el mensaje recibido
        datos = loads(msg.value().decode('utf-8'))

        # Incorporamos la columna category_value
        datos_enriquecidos = {
            'id': datos['id'],
            'title': datos['title'],
            'price': datos['price'],
            'stock': datos['stock'],
            'category_value': 'High' if datos['price'] > 50 else 'Standard'
        }

        # Enviamos el mensaje enriquecido al topic de destino
        data_str = dumps(datos_enriquecidos, ensure_ascii=False)
        data_bytes = data_str.encode('utf-8')
        producer.produce(topic=topic_destino, value=data_bytes)

        print(f"[RECIBIDO] {datos['title']} ${datos['price']} -> "
              f"[ENVIADO] category_value: {datos_enriquecidos['category_value']} "
              f"al topic {topic_destino}")

except KeyboardInterrupt:
    print("\nConsumer detenido por el usuario.")
finally:
    consumer.close()
    pending = producer.flush()
    if pending != 0:
        print(f"{pending} mensajes no se pudieron entregar.")
