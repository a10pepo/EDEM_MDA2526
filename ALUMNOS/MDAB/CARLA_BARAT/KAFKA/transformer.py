from confluent_kafka import Consumer, Producer
import json

conf_c = {'bootstrap.servers': 'localhost:9092', 'group.id': 'grupo-clima', 'auto.offset.reset': 'earliest'}
conf_p = {'bootstrap.servers': 'localhost:9092'}

consumer = Consumer(conf_c)
producer = Producer(conf_p)
consumer.subscribe(['lecturas-temperatura'])

print("Analizador de cadena de frío activo...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        if msg.error(): print(f"Error: {msg.error()}"); continue

        try:
            # Intentamos decodificar el JSON
            val = msg.value().decode('utf-8')
            datos = json.loads(val)
            
            # TRANSFORMACIÓN
            datos['unidad'] = 'Celsius'
            datos['almacen_id'] = 'VALENCIA_COLD_STORAGE'
            
            producer.produce('temperatura-enriquecida', value=json.dumps(datos).encode('utf-8'))
            producer.flush()
            print(f"Procesado: {datos['id_paquete']} a {datos['temp']}°C")
            
        except json.JSONDecodeError:
            print(f"Saltando mensaje no válido (no es JSON): {msg.value()}")
        except Exception as e:
            print(f"Error inesperado: {e}")

except KeyboardInterrupt:
    print("Deteniendo...")
finally:
    consumer.close()