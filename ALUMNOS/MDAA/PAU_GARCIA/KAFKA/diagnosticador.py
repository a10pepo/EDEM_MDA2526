from confluent_kafka import Producer
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

# Listado de averías
tipo_de_averia = [
    {"codigo_averia": 1, "gravedad": "baja", "pieza": "aire acondicionado", "desc_averia": "un fallo eléctrico ❄️"},
    {"codigo_averia": 2, "gravedad": "muy grave", "pieza": "motor", "desc_averia": "una grieta en el bloque 💥"},
    {"codigo_averia": 3, "gravedad": "muy grave", "pieza": "transmisión", "desc_averia": "una rotura completa de la caja de cambios ⚙️"},
    {"codigo_averia": 4, "gravedad": "media", "pieza": "frenos", "desc_averia": "las pastillas de freno desgastadas 🛑"},
    {"codigo_averia": 5, "gravedad": "baja", "pieza": "luces", "desc_averia": "una bombilla fundida 💡"},
    {"codigo_averia": 6, "gravedad": "baja", "pieza": "limpiaparabrisas", "desc_averia": "las escobillas deterioradas 🌧️"},
    {"codigo_averia": 7, "gravedad": "media", "pieza": "batería", "desc_averia": "la batería descargada 🔋"},
    {"codigo_averia": 8, "gravedad": "alta", "pieza": "turbo", "desc_averia": "un fallo en el turbocompresor 🚀"},
    {"codigo_averia": 9, "gravedad": "baja", "pieza": "radio", "desc_averia": "un problema con la radio 📻"},
    {"codigo_averia": 10, "gravedad": "media", "pieza": "suspensión", "desc_averia": "los amortiguadores desgastados 🔧"},
    {"codigo_averia": 11, "gravedad": "baja", "pieza": "escape", "desc_averia": "una fuga menor en el tubo de escape 💨"},
    {"codigo_averia": 12, "gravedad": "alta", "pieza": "embrague", "desc_averia": "el embrague patinando ⚡"}
]

def generar_matricula():
    numeros = ''.join(random.choices(string.digits, k=4))
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    return f"{numeros} {letras}"

def generar_averia():
    averia = random.choice(tipo_de_averia)
    if  averia["gravedad"]== "muy grave": 
        estado = "irreparable"
    else:
        estado = "reparable"

    return {
        "matricula": generar_matricula(),
        "codigo_averia": averia["codigo_averia"],
        "estado": estado,
        "gravedad": averia["gravedad"],
        "desc_averia": averia["desc_averia"],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def generar_diagnostico() : 
    try:
        averia = generar_averia()
        if averia["estado"] == "reparable":
            # Mostrar Reparable en azul
            print(Fore.BLUE + f"➡️ Ha entrado un encargo: El coche con matricula {averia['matricula']} tiene {averia['desc_averia']} ,  Alerta enviada al topic 'encargos_coches'  ({averia['timestamp']})")
        else:
            # Mostrar Irreparable en rojo
            print(Fore.RED + Style.BRIGHT + f"❌ COCHE IRREPARABLE: El coche con matricula {averia['matricula']} tiene {averia['desc_averia']} y no se puede reparar,  Alerta enviada al topic 'encargos_coches' con estado {averia['estado']}  ({averia['timestamp']})")
        # Enviar simpre la alerta al topic estado_ubicaciones, ya sea ok o alerta
        producer.produce(
                topic='encargos_coches',
                value=json.dumps(averia, ensure_ascii=False).encode('utf-8')
            )
        producer.flush()
    except KeyboardInterrupt:
        print(Fore.CYAN + "Productor detenido.")
    finally:
        producer.flush()

if __name__ == "__main__":
    while True:
        generar_diagnostico()
        time.sleep(3)
