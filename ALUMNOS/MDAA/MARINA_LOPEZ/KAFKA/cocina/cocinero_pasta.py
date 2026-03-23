from confluent_kafka import Consumer
import json
import time
from colorama import Fore, Style, init


# Inicializa colorama con autoreset
init(autoreset=True)


# Configuración del equipo de Pizzas
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'equipo_pasta',
    'auto.offset.reset': 'latest'
}
consumer = Consumer(conf)
consumer.subscribe(['pedidos_pasta'])

print(f"{Fore.GREEN}🍝 COCINERO PASTA: Listo y esperando tickets...")

try:
    while True:
        msg = consumer.poll(1.0)  # Espera hasta 1 segundo por un mensaje

        if msg is None:
            # No hay mensaje disponible en este momento, seguimos esperando
            continue

        if msg.error():
            # Si hay un error en el mensaje, lo mostramos
            print(f"Error al recibir pedido: {msg.error()}")
            continue

        # Si el mensaje es válido, mostramos su contenido
        # msg.value() devuelve los datos en bytes, por eso usamos decode('utf-8') para convertirlos a texto
        datos = json.loads(msg.value().decode('utf-8'))
        tipo_comida = datos['plato']['tipo']  
        nombre_plato = datos['plato']['nombre']
        mesa = datos['mesa']
        
        print(f"{Fore.GREEN}🔥 ¡Recibido! Marchando {Style.BRIGHT}{nombre_plato}{Style.NORMAL} para Mesa {mesa}")


except KeyboardInterrupt:
    print((f"{Fore.RED}Cocina cerrada por el usuario."))
finally:
    consumer.close()
