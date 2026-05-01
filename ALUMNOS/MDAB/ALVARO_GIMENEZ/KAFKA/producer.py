#Creamos un script de python que simula la lógica de negocio
#El script simula los logs de expedición de entregas en un SGA/WMS
#Cada expedición genera un JSON del resumen de la entrega y las diferencias (si las hubiera)

import time
import random
import json
from kafka import KafkaProducer

#Esperamos a que se levante kafka
time.sleep(15)

#Configuramos el objeto producer para enviar los mensajes
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

#Generamos un array (lista) de clientes y referencias para la simulación
clientes=["Customer 1", "Customer 2", "Customer 3", "Customer 4", "Customer 5", "Customer 6", "Customer 7", "Customer 8", "Customer 9", "Customer 10"]
referencias=["REF-001", "REF-002", "REF-003", "REF-004", "REF-005", "REF-006", "REF-007", "REF-008", "REF-009", "REF-010"]

#Creamos el generador de logs
def generador_entregas(order_id): 

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
        log_entrega={"timestamp": time.time(),
        "order_id": order_id,
        "customer": cliente, 
        "sku": referencia,
        "order_qnt": cantidad_pedido,
        "served_qnt": cantidad_servida,
        "diff": cantidad_pedido - cantidad_servida}

        return log_entrega

if __name__ == "__main__":
    #Contador para los order-id
    contador = 0
    try: 
        while True: 
            try:
                order_id = f"ORD-{contador}"
                log_entrega = generador_entregas(order_id)

                #Mandamos el mensaje al tópico
                producer.send('entregas', value=log_entrega)
                
                producer.flush() 
                
                print(f"Log enviado: {log_entrega}")

                contador += 1
                time.sleep(0.5)

            except Exception as e:
                print(f"Error en el envío individual: {e}")
                #Aquí NO ponemos finally ni close, para que el bucle siga

    except KeyboardInterrupt:
        print("\nDeteniendo el productor...")
    
    finally:
        print("Cerrando conexión con Kafka...")
        try:
            producer.close(timeout=10)
        except:
            pass