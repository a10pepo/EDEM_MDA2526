from confluent_kafka import Producer
import json
import time
import random
from colorama import Fore, Style, init

# Inicializa colorama
init(autoreset=True)

# Configuración del productor Kafka
conf = {
    'bootstrap.servers': 'localhost:9092'  # Ajusta según tu broker
}

producer = Producer(conf)
topic = 'pedidos_cocina'

# Lista de platos simuladas
platos = [
    {"id": 1, "tipo": "pizza", "nombre": "Pizza Margarita 🍕 "},
    {"id": 2, "tipo": "pasta", "nombre": "Pasta Carbonara 🍝"},
    {"id": 3, "tipo": "pizza", "nombre": "Pizza Pepperoni 🍕"},
    {"id": 4, "tipo": "pasta", "nombre": "Fettuccine Alfredo 🍝"},
    {"id": 5, "tipo": "pizza", "nombre": "Pizza Hawaiana 🍕"},
    {"id": 6, "tipo": "pasta", "nombre": "Fettuccini Caccio e Pepe 🍝"},
    {"id": 7, "tipo": "pasta", "nombre": "Fettuccine Pomodoro 🍝"},
    {"id": 8, "tipo": "pasta", "nombre": "Fettuccini Caccio e Pepe 🍝"}
]

print(f"{Fore.CYAN} CAMARERO: Empezando el servicio...")


try:
    id_pedido = 1
    while True:
        # Lógica de Probabilidad (20% VIP)
        if random.randint(1, 5) == 1: 
            tipo_cliente = "VIP"
            color_aviso = Fore.RED + Style.BRIGHT
        else:
            tipo_cliente = "Normal"
            color_aviso = Fore.WHITE
        
        
        pedido = {
            "id":id_pedido,
            "mesa": random.randint(1, 10),
            "plato": random.choice(platos),
            "hora": "14:30",
            "tipo_cliente": tipo_cliente
        }
        # Enviar simpre la alerta al topic
        pedido_str = json.dumps(pedido, ensure_ascii=False)
        pedido_bytes = pedido_str.encode('utf-8')
        producer.produce(topic, value = pedido_bytes)
       
        #print(f"{Fore.CYAN}📝 Comanda enviada: {Fore.WHITE}Mesa {pedido['mesa']} -> {Fore.YELLOW}{pedido['plato']['nombre']}")
        print(f"{Fore.CYAN}📝 Comanda enviada: {color_aviso}[{tipo_cliente}] Mesa {pedido['mesa']} -> {Fore.YELLOW}{pedido['plato']['nombre']}")      
        id_pedido += 1
        time.sleep(2)
except KeyboardInterrupt:
    print(f"{Fore.RED}Servicio detenido.")
finally:
    producer.flush()

