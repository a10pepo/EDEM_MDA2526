from confluent_kafka import Producer
import json
import time
import random

#Configuramos el producer

conf = {
    'bootstrap.servers': 'localhost:9092'  #Puerto 95 para evitar conflicto con DataProject

}
producer = Producer(conf)


#definimos las habitaciones que contienen sensores domóticos y los eventos que pueden generar triggers
habitaciones = [
    {"id": 1, "nombre": "salon", "tipo": 'interior'},
    {"id": 2, "nombre": "entrada", "tipo": 'interior'},
    {"id": 3, "nombre": "jardin", "tipo": 'exterior'},
    {"id": 4, "nombre": "porche", "tipo": 'exterior'},
    {"id": 5, "nombre": "cocina", "tipo": 'interior'},
    {"id": 6, "nombre": "dormitorio", "tipo": 'interior'}]

eventos_interior = [
    "movimiento detectado",
    "temperatura baja",
    "temperatura alta"]

eventos_exterior = [
    "movimiento detectado",
    "lluvia detectada",
    "viento fuerte"]

def generar_evento():
    habitacion = random.choice(habitaciones)
    if random.randint(1,7) == 1:
        if habitacion["tipo"] == 'interior':
            evento = random.choice(eventos_interior)
        else:
            evento = random.choice(eventos_exterior)
    else:
        evento = "sin_evento"

    evento_data = {
        "habitacion_id": habitacion["id"],
        "habitacion_nombre": habitacion["nombre"],
        "tipo_habitacion": habitacion["tipo"],
        "evento": evento,
        "timestamp": int(time.time())
    }
    return evento_data

print("Iniciando productor de alertas...")

try:
    while True:
        evento = generar_evento()
        if evento["evento"] == "sin_evento":
            print(f"Sin eventos en {evento['habitacion_nombre']}. No se requieren acciones.")
            evento_json = json.dumps(evento)
            # producer.produce('eventos_domoticos', key=str(evento["habitacion_id"]), value=evento_json)
            # producer.flush()
            # print(f"Evento enviado: {evento_json}")
        
        else:
            print(f"Evento detectado en {evento['habitacion_nombre']}: {evento['evento']}. Se requiere una acción, enviando mensaje")
            evento_json = json.dumps(evento)
        
            producer.produce('eventos_domoticos', key=str(evento["habitacion_id"]), value=evento_json)
            producer.flush()
            print(f"Evento enviado: {evento_json}")
        time.sleep(5)  

except KeyboardInterrupt:
    print("Productor detenido.")
finally:
    producer.flush()




