from confluent_kafka import Producer
import json
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

# Lista de ubicaciones simuladas
ubicaciones = [
    {"id": 1, "tipo": "hogar", "nombre": "Casa Pérez"},
    {"id": 2, "tipo": "hogar", "nombre": "Casa López"},
    {"id": 3, "tipo": "almacén", "nombre": "Almacén Central"},
    {"id": 4, "tipo": "fábrica", "nombre": "Fábrica Norte"},
    {"id": 5, "tipo": "fábrica", "nombre": "Fábrica Sur"},
    {"id": 6, "tipo": "hogar", "nombre": "Casa García"},
    {"id": 7, "tipo": "almacén", "nombre": "Almacén Este"},
    {"id": 8, "tipo": "hogar", "nombre": "Casa Martínez"}
]

# Diccionario de alertas con iconos
alertas = {
    "robo": "🦹",
    "fuego": "🔥",
    "inundación": "💧"
}

def generar_mensaje():
    ubicacion = random.choice(ubicaciones)
    if random.randint(1, 20) == 1:  # Probabilidad de alerta real (~5%)
        estado = "alerta"
        alerta_tipo = random.choice(list(alertas.keys()))
        alerta_icono = alertas[alerta_tipo]
    else:
        estado = "ok"
        alerta_tipo = None
        alerta_icono = None

    return {
        "ubicacion_id": ubicacion["id"],
        "tipo": ubicacion["tipo"],
        "nombre": ubicacion["nombre"],
        "estado": estado,
        "alerta_tipo": alerta_tipo,
        "alerta_icono": alerta_icono,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

print(Fore.CYAN + "Iniciando productor de alertas...")

try:
    while True:
        mensaje = generar_mensaje()
        if mensaje["estado"] == "ok":
            # Mostrar OK en azul
            print(Fore.BLUE + f"Todo bien en {mensaje['nombre']}, Estado OK enviado al topic Alerta enviada al topic \'estado_ubicaciones\'  ({mensaje['timestamp']})")
        else:
            # Mostrar alerta en rojo y negrita
            print(Fore.RED + Style.BRIGHT +
                  f"🚨 ALERTA: {mensaje['alerta_icono']} {mensaje['alerta_tipo'].upper()} en {mensaje['nombre']}({mensaje['timestamp']})")
            print(Fore.YELLOW + f"✅ Alerta enviada al topic 'estado_ubicaciones'")
            
        # Enviar simpre la alerta al topic estado_ubicaciones, ya sea ok o alerta
        producer.produce(
                topic='estado_ubicaciones',
                value=json.dumps(mensaje, ensure_ascii=False).encode('utf-8')
            )
        producer.flush()
        time.sleep(1)
except KeyboardInterrupt:
    print(Fore.CYAN + "Productor detenido.")
finally:
    producer.flush()