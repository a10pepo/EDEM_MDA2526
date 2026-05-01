#Creamos un consumidor que leerá mensajes del tópico de kafka y añade algunos cálculos
#Añade el % de rotura del pedido cantidad_rotura/cantidad_pedido y asigna en función de rangos un nivel de criticidad (leve, grave, muy grave)

import json
from kafka import KafkaConsumer, KafkaProducer
import time 

#Esperamos a que se levante kafka
time.sleep(20)

#Configuramos el consumidor
#Nos identificamos como group_id_1 para que kafka nos recuerde si se cae el servicio
#Hacemos auto_offset_reset latest para que si el servicio se cae no se sature de mensajes antiguos al arrancar, solo procesará los nuevos
consumer = KafkaConsumer(
    'entregas',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='latest',
    group_id='group_id_1')

#Configuramos del Productor (para enviar al nuevo tópico)
#Este enviará las alertas procesadas
producer_alerts = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8'))

#El consumer realmente es un puntero que apunta a la cola, al punto de la cola que toque (offset)
#Es un OBJETO, iterable, que guarda la conexión y dirección al punto de la cola donde te quedaste
#También recibe el nombre de simplemente "offset"

try:
    #Este bucle es infinito, se queda pillado esperando mensajes
    for message in consumer:
        #Extraemos el JSON (que ya viene deserializado gracias al lambda)
        datos = message.value
        
        #Lógica de negocio (Cálculos de criticidad)
        qnt_pedido = datos.get('order_qnt', 0)
        qnt_diff = datos.get('diff', 0)

        #Manejamos error división /0         
        if qnt_pedido == 0: 
            porcentaje_rotura=0
        else: 
            porcentaje_rotura = (qnt_diff / qnt_pedido) * 100
        
        if porcentaje_rotura == 0:
            nivel = "OK"
        elif porcentaje_rotura < 20:
            nivel = "LEVE"
        elif porcentaje_rotura < 50:
            nivel = "GRAVE"
        else:
            nivel = "MUY GRAVE"

        #Creamos el nuevo mensaje con la información enriquecida para enviar a KSQL
        alerta = {
            "order_id": datos.get('order_id'),
            "porcentaje_rotura": round(porcentaje_rotura, 2),
            "nivel_criticidad": nivel,
            "timestamp": datos.get('timestamp')
        }

        #MANDAMOS AL NUEVO TÓPICO PARA KSQL
        producer_alerts.send('alertas_entregas', value=alerta)
        producer_alerts.flush()
        print(f"Enviado a KSQL: {nivel} | {datos['order_id']}", flush=True)

        #Lo mostramos por la consola de Docker, flusheamos para que lo muestre
        print(f"{nivel} | Orden: {datos['order_id']} | Rotura: {porcentaje_rotura:.2f}%", flush=True)

except KeyboardInterrupt:
    print("Consumidor detenido manualmente.")
finally:
    consumer.close()
