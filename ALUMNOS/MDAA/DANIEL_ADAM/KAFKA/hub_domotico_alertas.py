from confluent_kafka import Consumer, Producer
import json
import logging
import time

# Configuración del consumidor
conf_consumer = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': f'grupo_alertas_1',
    'auto.offset.reset': 'latest'
}
consumer = Consumer(conf_consumer)
consumer.subscribe(['eventos_domoticos'])

# Configuración del productor
conf_producer = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf_producer)

def enviar_alerta(datos):
    alerta_json = json.dumps(datos)
    if datos.get("tipo_habitacion") == 'interior':
        alerta_json = json.dumps(datos)
        producer.produce('eventos_interior', key=str(datos["habitacion_id"]), value=alerta_json)
    else:
        alerta_json = json.dumps(datos)
        producer.produce('eventos_exterior', key=str(datos["habitacion_id"]), value=alerta_json)
    producer.flush()

print("Iniciando HUB domotico para gestión de alertas...")

try:
    while True:
        momento = time.strftime("%Y-%m-%d %H:%M:%S")
        message = consumer.poll(1.0)
        if message is None:
            continue
        if message.error():
            print(f"Error: {message.error()}")
            continue

        evento = json.loads(message.value().decode('utf-8'))
        if evento.get("evento") == "movimiento detectado":
            evento["accion"] = "Encender luces"
        if evento.get("evento") == "temperatura baja":
            evento["accion"] = "Encender radiadores"
        if evento.get("evento") == "temperatura alta":
            evento["accion"] = "Encender aire acondicionado"
        if evento.get("evento") == "lluvia detectada":
            evento["accion"] = "Apagar aspersores"
        if evento.get("evento") == "viento fuerte":
            evento["accion"] = f"Se ha detectado viento fuerte a las {momento} en {evento.get('habitacion_nombre')}. Por favor, cierre las ventanas."
            


        # Mensaje detallado
        print(f"[{momento}] 📡 {evento["evento"]} en {evento["habitacion_nombre"]}. Acción requerida: {evento["accion"]}")
        enviar_alerta(evento)

except KeyboardInterrupt:
    print("HUB domotico detenido.")
finally:
    consumer.close()

