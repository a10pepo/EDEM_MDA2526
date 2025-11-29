from confluent_kafka import Producer, Consumer
import json
import string
import time
import random
from colorama import Fore, Style, init

posibles_piezas_necesarias = {
    1: ["fusible", "relé", "cableado", "módulo de control del A/C"],
    4: ["pastillas de freno", "discos de freno (si procede)", "líquido de frenos", "sensores de desgaste"],
    5: ["bombilla (especificación correcta)", "portalámparas", "fusible de iluminación"],
    6: ["escobillas limpiaparabrisas", "brazo de limpiaparabrisas (si está dañado)"],
    7: ["batería nueva (especificación correcta)", "terminales/borne", "comprobación o reemplazo alternador si procede"],
    8: ["turbo completo (o kit de reparación)", "juntas y retenes", "tubos intercooler/abrazaderas"],
    9: ["unidad de radio/autoradio (reemplazo)", "antena (si procede)", "fusible de radio"],
    10: ["amortiguadores", "muelles (si procede)", "kieletas/bieletas", "kit de montaje de amortiguador"],
    11: ["tramo de tubo de escape de repuesto", "junta de escape", "abrazaderas/bridas"],
    12: ["kit de embrague (disco, plato, collarín)", "volante motor (si está dañado)"]
}
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
consumer.subscribe(['encargos_coches'])
consumer.subscribe(['encargos_piezas'])



def encargar_piezas(mensaje, pieza):
    producer.produce(
        topic='encargo_piezas',
        value=json.dumps(mensaje, ensure_ascii=False).encode('utf-8'),
        headers=[("producer", "taller")]
    )
    producer.flush()
    print(Fore.YELLOW + f" 🔄 FALTAN PIEZAS. Encargo de {pieza} enviado al proveedor (topic 'encargo_piezas')")

def reparacion(mensaje):
    producer.produce(
        topic='encargos_finalizados',
        value=json.dumps(mensaje,ensure_ascii=False).encode('utf-8')
    )
    producer.flush()
    print(Fore.GREEN + f"✅ Reparación del vehiculo {mensaje["matricula"]} finalizada (topic 'encargos_finalizados')")

def faltan_piezas(gravedad):
    if gravedad == "alta":
        p = 70
    elif gravedad == "media":
        p = 50
    elif gravedad in "baja":
        p = 20
    else:
        p = 100
    if random.randint(0,100) > p


if __name__ == "__main__":
    try:
        while True:
            msg = consumer.poll(1.0)
            if dict(msg.headers() or {}).get("producer") == "taller":
                continue
            if msg is None:
                continue
            if msg.error():
                print(Fore.RED + f"Error en el mensaje: {msg.error()}")
                continue
            encargo = json.loads(msg.value().decode('utf-8'))
            if msg.topic() == "encargos_coches":
                print(Fore.WHITE + f"👨🏻‍🔧 Reparación del coche con matricula {msg["matricula"]} en marcha.")
                piezas = faltan_piezas(encargo.get("gravedad"))
                if piezas:
                    piezas = posibles_piezas_necesarias.get(encargo.get("codigo_averia"), [])
                    pieza = random.choice(piezas)
                    encargo["pieza"] = pieza
                    encargar_piezas(encargo,pieza)
                else :
                    reparacion(encargo)
            if msg.topic() == "encargos_piezas":
                print(Fore.CYAN + f"⚙️ Ha llegado la pieza {encargo.get("pieza")}. Reparación del coche con matricula {msg["matricula"]} en marcha.")
                reparacion(encargo)

    except:
        print(Fore.CYAN + "Gestor detenido.")
