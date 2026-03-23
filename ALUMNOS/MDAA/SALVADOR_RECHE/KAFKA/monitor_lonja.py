from confluent_kafka import Consumer
import json
from colorama import Fore, Style, init

init(autoreset=True)

# Asegúrate de que este es el nombre EXACTO que le diste en KSQL
TOPIC_FINAL = 'STREAM_MERCADO_FRESCO'

# Configuración
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo_lonja_v2', # Cambio el grupo para que no lea mensajes viejos corruptos
    'auto.offset.reset': 'latest'
}

consumer = Consumer(conf)
consumer.subscribe([TOPIC_FINAL])

print(Fore.MAGENTA + Style.BRIGHT + f"🏪 PANTALLA DE LA LONJA (Escuchando: {TOPIC_FINAL})")
print("------------------------------------------------")

try:
    while True:
        msg = consumer.poll(1.0)
        
        # 1. Si no hay mensaje, seguimos
        if msg is None:
            continue
        
        # 2. Si hay error de Kafka, lo imprimimos y seguimos
        if msg.error():
            print(Fore.RED + f"Error de Kafka: {msg.error()}")
            continue

        # 3. Obtenemos el valor crudo (bytes)
        raw_value = msg.value()
        
        # 4. Si el mensaje está vacío (None o vacío), saltamos
        if raw_value is None or len(raw_value) == 0:
            continue

        try:
            # Intentamos decodificar
            decoded_str = raw_value.decode('utf-8')
            d = json.loads(decoded_str)
            
            # --- LÓGICA DE VISUALIZACIÓN ---
            # KSQL a veces pone las claves en MAYÚSCULAS, probamos ambas formas
            especie = d.get('ESPECIE') or d.get('especie')
            peso = d.get('PESO') or d.get('peso')
            icono = d.get('ICONO') or d.get('icono') or "📦"
            
            if especie == "Tiburón":
                print(Fore.RED + f"{icono} TIBURÓN FRESCO - {peso}kg (Venta directa)")
            elif especie == "Atún":
                print(Fore.GREEN + f"{icono} ATÚN PREMIUM - {peso}kg (Calidad Sashimi)")
            else:
                # Si llega algo raro pero es JSON válido, lo mostramos en gris
                print(Fore.LIGHTBLACK_EX + f"Recibido otro dato: {d}")

        except json.JSONDecodeError:
            
            print(Fore.YELLOW + f"⚠️  Mensaje ignorado (No es JSON válido): {raw_value}")
        except Exception as e:
            print(Fore.RED + f"⚠️  Error procesando mensaje: {e}")

except KeyboardInterrupt:
    print("\nCerrando lonja.")
finally:
    consumer.close()