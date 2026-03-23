#Creamos un script de python que simula la lógica de negocio
#El script simula los logs de expedición de entregas en un SGA/WMS
#Cada expedición genera un JSON del resumen de la entrega y las diferencias (si las hubiera)

import time
import random
import json
from kafka import KafkaProducer

#Configuramos el objeto producer para enviar los mensajes
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
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

#Ejecutor principal (no sería necesario, no vamos a reutilizar las funciones, pero es buena práctica)
if __name__ == "__main__":

    #Contador para los order-id, en cada ejecución del servicio se reiniciará¡! Ojo consistencia de ids si escalamos funcionalidad
    contador=0

    while True: 

        try:
            order_id = f"ORD-{contador}"
            log_entrega = generador_entregas(order_id)

            #Mandamos el mensaje (log de simulación) al tópico de KAFKA
            producer.send('entregas', value=log_entrega)

            #Sacamos un log resumen por pantalla
            print(f"Log enviado: {log_entrega}")

            #Aumentamos el contador
            contador += 1
    
            #Dormimos medio segundo hasta el próximo log
            time.sleep(0.5)

        #Manejamos los posibles errores que pueden darse
        except KeyboardInterrupt:
            print("Simulación detenida por el usuario.")
        except Exception as e:
            print(f"Error inesperado: {e}")
        finally:
            producer.close()