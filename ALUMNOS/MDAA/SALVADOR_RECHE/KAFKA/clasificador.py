from confluent_kafka import Consumer, Producer
import json
from colorama import Fore, Style, init

init(autoreset=True)

# Lee de 'ingesta_pesca' -> Escribe en 'pesca_clasificada'
consumer = Consumer({'bootstrap.servers': 'localhost:9092', 'group.id': 'grupo_calidad', 'auto.offset.reset': 'latest'})
producer = Producer({'bootstrap.servers': 'localhost:9092'})

consumer.subscribe(['ingesta_pesca'])

print(Fore.CYAN + "🏭 Cinta transportadora de Clasificación en marcha...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        
        datos = json.loads(msg.value().decode('utf-8'))
        peso = datos['peso_kg']
        especie = datos['especie']
        
        # --- LÓGICA DE NEGOCIO ---
        destino = ""
        motivo = ""
        
        if especie == "Tiburón":
            destino = "NATURAL"
            motivo = "Aleta/Filete"
            color_print = Fore.RED # Rojo para tiburón
            
        elif especie == "Atún":
            if peso > 60:
                destino = "NATURAL"
                motivo = "Peso Premium"
                color_print = Fore.GREEN # Verde para lo bueno
            else:
                destino = "CONSERVA"
                motivo = "Peso bajo"
                color_print = Fore.YELLOW # Amarillo para latas

        # Creamos el mensaje enriquecido
        datos_finales = {
            "especie": especie,
            "peso": peso,
            "destino": destino, # <--- CAMPO NUEVO IMPORTANTE
            "motivo": motivo,
            "icono": datos['icono']
        }
        
        # Enviamos al siguiente topic
        producer.produce(topic='pesca_clasificada', value=json.dumps(datos_finales).encode('utf-8'))
        producer.flush()
        
        print(color_print + f"📦 {especie} ({peso}kg) -> Para: {destino} ({motivo})")

except KeyboardInterrupt:
    print("Cinta detenida.")