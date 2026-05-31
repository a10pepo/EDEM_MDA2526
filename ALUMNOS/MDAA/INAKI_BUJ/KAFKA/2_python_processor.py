from confluent_kafka import Consumer, Producer
import json
import time
import random
from colorama import Fore, Style, init

init(autoreset=True)

# --- CONFIGURACIÓN ---
# Consumidor: Lee del puerto 9092 (tu puerto externo)
conf_consumer = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'python_enricher_group',
    'auto.offset.reset': 'latest'
}

# Productor: También envía al 9092
conf_producer = {
    'bootstrap.servers': 'localhost:9092'
}

consumer = Consumer(conf_consumer)
producer = Producer(conf_producer)

# Topics
input_topic = 'raw_transactions'
output_topic = 'enriched_transactions'

consumer.subscribe([input_topic])

print(Fore.CYAN + Style.BRIGHT + "⚙️  PROCESADOR INTELIGENTE INICIADO...")
print(Fore.CYAN + "   Esperando transacciones para calcular riesgo...")

try:
    while True:
        msg = consumer.poll(1.0)
        
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue

        # 1. Decodificar mensaje original
        data = json.loads(msg.value().decode('utf-8'))
        
        # --- LÓGICA DE NEGOCIO (ENRIQUECIMIENTO) ---
        
        # Regla 1: Convertir todo a USD (Simulación)
        # Asumimos que si no es US, hay que convertir
        monto = data['monto_original']
        if data['pais_origen'] != 'US':
            monto_usd = round(monto * 1.1, 2) # Conversión simulada
        else:
            monto_usd = monto

        # Regla 2: Calcular Score de Riesgo (0-100)
        # Si el monto es alto (>200) o el país es de riesgo, sube el score
        score = 10
        if monto_usd > 200:
            score += 40
        if data['es_fraude']:
            score = 99 # Si Kaggle dice que es fraude, riesgo máximo
        elif data['pais_origen'] in ['MX', 'CO', 'AR']:
            score += 20 # Países con mayor fricción (simulado)

        # Crear nuevo JSON enriquecido
        data_enriched = {
            "id": data['id_transaccion'],
            "cliente": data['cliente'],
            "monto_usd": monto_usd,
            "pais": data['pais_origen'],
            "riesgo_calculado": score,
            "origen_dato": "Python Processor"
        }
        
        # -------------------------------------------

        # Enviar al siguiente topic
        producer.produce(output_topic, json.dumps(data_enriched).encode('utf-8'))
        producer.flush()

        # Feedback Visual (Amarillo para diferenciar)
        print(Fore.YELLOW + f"🔄 Procesado: {data_enriched['id']} | "
              f"Riesgo: {score}/100 | USD: {monto_usd}")

except KeyboardInterrupt:
    print("Procesador detenido.")
finally:
    consumer.close()