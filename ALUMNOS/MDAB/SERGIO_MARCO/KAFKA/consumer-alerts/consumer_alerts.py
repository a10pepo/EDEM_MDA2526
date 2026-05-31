# ============================================
# CONSUMER ALERTS - Lee de inventory_alerts
# e imprime las alertas por pantalla
# ============================================
# Este consumer lee los mensajes filtrados por KSQL:
# productos con category_value = 'High' y stock < 10
# y los imprime por pantalla

from json import loads
from confluent_kafka import Consumer

# ============================================
# Configuracion del consumidor
# ============================================
config = {
    'bootstrap.servers': 'kafka:29092',
    'group.id': 'grupo-alertas',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(config)
topic_kafka = 'inventory_alerts'
consumer.subscribe([topic_kafka])

# ============================================
# Bucle principal
# ============================================

print(f"Esperando alertas del topic '{topic_kafka}'...")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print(f"Error al recibir mensaje: {msg.error()}")
            continue

        datos = loads(msg.value().decode('utf-8'))

        print(f"[ALERTA] Producto: {datos['TITLE']} | "
              f"Precio: ${datos['PRICE']} | "
              f"Stock: {datos['STOCK']} | "
              f"Categoria: {datos['CATEGORY_VALUE']}")

except KeyboardInterrupt:
    print("\nConsumer de alertas detenido por el usuario.")
finally:
    consumer.close()
