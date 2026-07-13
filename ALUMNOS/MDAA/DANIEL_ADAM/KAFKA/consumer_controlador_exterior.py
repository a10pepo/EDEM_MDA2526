from confluent_kafka import Consumer
import json
import time

# Configuración del consumidor
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo_exterior',  
    'auto.offset.reset': 'latest'
}
consumer = Consumer(conf)
consumer.subscribe(['eventos_exterior'])

print("Sistema domótico exterior escuchando eventos...")

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
            print(f"[{momento}] Movimiento detectado en {datos.get('habitacion_nombre')}. 💡 Luces exteriores del {datos.get('habitacion_nombre')} encendidas ✅.")
        if datos.get("evento") == "lluvia detectada":
            print(f"[{momento}] Lluvia detectada en {datos.get('habitacion_nombre')}. ⛲ Aspersores apagados ✅.")
        if datos.get("evento") == "viento fuerte":
            print(f"[{momento}] Viento fuerte detectado en {datos.get('habitacion_nombre')}. 🍃 Alerta enviada al usuario para que cierre las ventanas 📲.")
            


except KeyboardInterrupt:
    print("Controlador domotico interior detenido.")
finally:
    consumer.close()