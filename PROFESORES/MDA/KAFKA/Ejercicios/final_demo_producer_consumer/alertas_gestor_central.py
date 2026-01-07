from confluent_kafka import Consumer, Producer
import json
import logging
from colorama import Fore, Style, init
import time

# Inicializa colorama
init(autoreset=True)

# Configuración de logs
logging.basicConfig(filename='alertas.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Configuración del productor
conf_producer = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf_producer)

# Función para enviar alerta
def enviar_alerta(mensaje):
    producer.produce(
        topic='alertas_confirmadas',
        value=json.dumps(mensaje, ensure_ascii=False).encode('utf-8')
    )
    producer.flush()
    print(Fore.YELLOW + f"✅ Alerta enviada al topic 'alertas_confirmadas'")

# Configuración del consumidor
conf_consumer = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': f'grupo_alertas_{int(time.time())}',
    'auto.offset.reset': 'latest'
}
consumer = Consumer(conf_consumer)
consumer.subscribe(['estado_ubicaciones'])

print(Fore.CYAN + "Iniciando gestor de alertas...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(Fore.RED + f"Error en el mensaje: {msg.error()}")
            continue

        datos = json.loads(msg.value().decode('utf-8'))
        nombre = datos.get("nombre")
        estado = datos.get("estado")
        alerta_tipo = datos.get("alerta_tipo")
        alerta_icono = datos.get("alerta_icono")

        if estado == "ok":
            print(Fore.GREEN + f"Todo bien en {nombre}")
        elif estado == "alerta":
            # Mostrar alerta con icono 🚨 + tipo + icono específico
            print(Fore.RED + Style.BRIGHT +
                  f"🚨 ALERTA detectada en {nombre} | Tipo: {alerta_icono} {alerta_tipo.upper()}")
            logging.info(f"Alerta detectada: {datos}")
            enviar_alerta(datos)

except KeyboardInterrupt:
    print(Fore.CYAN + "Gestor detenido.")
finally:
    consumer.close()