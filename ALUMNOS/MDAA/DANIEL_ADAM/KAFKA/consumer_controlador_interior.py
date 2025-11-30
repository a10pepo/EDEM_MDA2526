from confluent_kafka import Consumer
import json
import time

# Configuración del consumidor
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo_interior',  
    'auto.offset.reset': 'latest'
}
consumer = Consumer(conf)
consumer.subscribe(['eventos_interior'])

print("Sistema domótico interior escuchando eventos...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue

        datos = json.loads(msg.value().decode('utf-8'))
        momento = time.strftime("%Y-%m-%d %H:%M:%S")
        if datos.get("evento") == "movimiento detectado":
            print(f"[{momento}] Movimiento detectado en {datos.get('habitacion_nombre')}. 💡 Luces de {datos.get('habitacion_nombre')} encendidas ✅.")
        if datos.get("evento") == "temperatura baja":
            print(f"[{momento}] Temperatura baja en {datos.get('habitacion_nombre')}. 🔥 Radiadores de {datos.get('habitacion_nombre')} encendidos ✅.")
        if datos.get("evento") == "temperatura alta":
            print(f"[{momento}] Temperatura alta en {datos.get('habitacion_nombre')}. ❄️  Aire acondicionado de {datos.get('habitacion_nombre')} encendido ✅.")
            


except KeyboardInterrupt:
    print("Controlador domotico interior detenido.")
finally:
    consumer.close()