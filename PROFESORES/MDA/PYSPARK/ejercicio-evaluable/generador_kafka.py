# ============================================
# GENERADOR DE DATOS PARA KAFKA (EJERCICIO EVALUABLE)
# ============================================
# Este script genera datos simulados de operaciones de e-commerce y los envía a un tópico de Kafka.
# Autor: Nacho Reyes
#
# Requisitos:
#   - Tener Kafka y Zookeeper en ejecución (puedes usar Docker Compose)
#   - Instalar la librería confluent-kafka: pip install confluent-kafka
# ============================================

import time
import random
from datetime import datetime
from json import dumps
from confluent_kafka import Producer

# Configuración del productor
config = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'generador-evaluable'
}
producer = Producer(config)

topic_kafka = 'operaciones_ecommerce'

# Listas de ejemplo para simular datos
productos = ['Portátil', 'Smartphone', 'Tablet', 'Auriculares', 'Monitor', 'Teclado', 'Ratón', 'Impresora']
usuarios = [f'user_{i:03d}' for i in range(1, 21)]
metodos_pago = ['Tarjeta', 'PayPal', 'Transferencia', 'Criptomoneda']
estados = ['Completada', 'Pendiente', 'Cancelada']

for i in range(50):
    data = {
        'id_operacion': f'OP{i+1:04d}',
        'usuario': random.choice(usuarios),
        'producto': random.choice(productos),
        'cantidad': random.randint(1, 5),
        'precio_unitario': round(random.uniform(20, 1200), 2),
        'metodo_pago': random.choice(metodos_pago),
        'estado': random.choices(estados, weights=[0.7, 0.2, 0.1])[0],
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    data['total'] = round(data['cantidad'] * data['precio_unitario'], 2)
    data_str = dumps(data, ensure_ascii=False)
    data_bytes = data_str.encode('utf-8')
    producer.produce(topic=topic_kafka, value=data_bytes)
    print(f"Enviando: {data}")
    time.sleep(0.5)

producer.flush()
print("Todos los mensajes han sido enviados.")
