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
    'auto.offset.reset': 'earliest' 
}
consumer = Consumer(conf_consumer)
consumer.subscribe([ 'encargos_piezas'])

def suministrar_piezas(mensaje, pieza):
    producer.produce(
        topic='encargos_piezas',
        value=json.dumps(mensaje, ensure_ascii=False).encode('utf-8'),
        headers=[("producer", "proveedor")]
    )
    producer.flush()
    print(Fore.GREEN + f" 📭 El pedido de {pieza} ha llegado a su destino")


if __name__ == "__main__":
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(Fore.RED + f"Error en el mensaje: {msg.error()}")
                continue
            headers = dict(msg.headers() or [])
            producer_hdr = headers.get("producer")
            if isinstance(producer_hdr, bytes):
                producer_hdr = producer_hdr.decode("utf-8")
            if producer_hdr == "proveedor":
                continue
            encargo = json.loads(msg.value().decode('utf-8'))
            print(Fore.BLUE + f" 📥 Pedido de {encargo.get("pieza")} recibido. Pieza en camino")
            time.sleep(3) # simular tiempo de envío
            suministrar_piezas(encargo, encargo.get("pieza"))

    except Exception as e:
        print(Fore.CYAN + f"Gestor detenido: {e}")