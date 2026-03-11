# ============================================
# PRODUCER - Productos aleatorios (DummyJSON)
# ============================================
# Consulta la API de DummyJSON cada segundo, obtiene
# un producto aleatorio y lo envia al topic "inventory_raw"

import time
import random
from json import dumps
from datetime import datetime, timezone

import requests
from confluent_kafka import Producer

# ============================================
# Configuracion del productor
# ============================================
config = {
    'bootstrap.servers': 'kafka:29092',
    'client.id': 'product-producer'
}

producer = Producer(config)
topic_kafka = 'inventory_raw'

# ============================================
# Configuracion de DummyJSON API
# ============================================

DUMMYJSON_URL = 'https://dummyjson.com/products'
TOTAL_PRODUCTOS = 194
INTERVALO_SEGUNDOS = 1

# ============================================
# Bucle principal
# ============================================

try:
    while True:
        product_id = random.randint(1, TOTAL_PRODUCTOS)
        response = requests.get(f"{DUMMYJSON_URL}/{product_id}", timeout=10)
        producto = response.json()

        data = {
            'id': producto['id'],
            'title': producto['title'],
            'category': producto['category'],
            'price': producto['price'],
            'discountPercentage': producto['discountPercentage'],
            'rating': producto['rating'],
            'stock': producto['stock'],
            'brand': producto.get('brand', 'N/A'),
            'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        }

        data_str = dumps(data, ensure_ascii=False)
        data_bytes = data_str.encode('utf-8')

        producer.produce(topic=topic_kafka, value=data_bytes)

        print(f"Enviando datos: {data} al topic {topic_kafka}")

        time.sleep(INTERVALO_SEGUNDOS)

except KeyboardInterrupt:
    print("\nProducer detenido por el usuario.")
finally:
    pending = producer.flush()
    if pending != 0:
        print(f"{pending} mensajes no se pudieron entregar.")
