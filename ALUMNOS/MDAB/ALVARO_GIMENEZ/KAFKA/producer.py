#Creamos un script de python que simula la lógica de negocio
#El script simula los logs de expedición de entregas en un SGA/WMS
#Cada expedición genera un JSON del resumen de la entrega y las diferencias (si las hubiera)

import time
import random
import json
from kafka import KafkaProducer

#Configuramos el objeto producer para enviar los mensaje
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

#Generamos un array (lista) de clientes y referencias para la simulación
clientes=["Cliente 1", "Cliente 2", "Cliente 3", "Cliente 4", "Cliente 5", "Cliente 6", "Cliente 7", "Cliente 8", "Cliente 9", "Cliente 10"]
referencias=["REF-001", "REF-002", "REF-003", "REF-004", "REF-005", "REF-006", "REF-007", "REF-008", "REF-009", "REF-010"]

#Creamos el generador de logs
def generador_entregas(): 
     while True:
        cliente = random.choice(clientes)
        referencia=random.choice(referencias)
        cantidad_pedido = random.randint(1, 100)

        #Para que sea mas realista, solo el 5% de las entregas tienen diferencias, el resto sirven al 100%
        #Este es un ratio relativamente habitual en gran consumo
        if random.random() < 0.05 :
            cantidad_servida = random.randint(0, cantidad_pedido)
        else:
            cantidad_servida = cantidad_pedido

        #Generamos el paquete de datos a enviar (log simulado)
        log_entrega={"cliente": cliente, 
        "referencia": referencia,
        "cantidad_pedido", cantidad_pedido,
        "cantidad_servida", cantidad_servida
        "Diferencia", cantidad_pedido - cantidad_servida}