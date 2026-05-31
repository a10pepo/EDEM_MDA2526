from confluent_kafka import Producer, Consumer
import json
import string
import time
import random
from colorama import Fore, Style, init

# Inicializa colorama con autoreset
init(autoreset=True)

# Configuración del productor Kafka
conf = {
    'bootstrap.servers': 'localhost:9092'  # Ajusta según tu broker
}
producer = Producer(conf)

conf_consumer = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': f'grupo_alertas_{int(time.time())}',
    'auto.offset.reset': 'latest' 
}
consumer = Consumer(conf_consumer)
consumer.subscribe([ 'encargos_finalizados','encargos_cancelados'])
def lowercase(obj):
    if isinstance(obj, dict):
        return {str(k).lower(): lowercase(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [lowercase(i) for i in obj]
    return obj

def avisar_cliente(mensaje):
    producer.produce(
        topic='avisos_cliente',
        value=json.dumps(mensaje, ensure_ascii=False).encode('utf-8')
    )
    producer.flush()
    if mensaje.get("gravedad") != 'muy alta' :
        print(Fore.GREEN + f"📲 Enviando mensaje al cliente dueño del vehículo con matricula {mensaje.get("matricula")}")
    else:
        print(Fore.RED + f"❌📲 Enviando mensaje de cancelación al cliente dueño del vehículo con matricula {mensaje.get("matricula")}")


if __name__ == "__main__":
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(Fore.RED + f"Error en el mensaje: {msg.error()}")
                continue

            encargo = json.loads(msg.value().decode('utf-8'))
            if msg.topic() == 'encargos_finalizados':
                print(Fore.BLUE + f"El coche con matrícula {encargo.get("matricula")} esta listo para que su dueño lo recoja")
                avisar_cliente(encargo)
                continue
            if msg.topic() == 'encargos_cancelados' :
                encargo = lowercase(encargo)
                print(Fore.LIGHTRED_EX + f"El coche con matrícula {encargo.get("matricula")} no puede ser reparado")
                avisar_cliente(encargo)
                continue
            

    except Exception as e:
        print(Fore.CYAN + f"Gestor detenido: {e}")