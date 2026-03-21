import os
import requests
import json
import time
from dotenv import load_dotenv
from kafka import KafkaProducer

# 1. Cargamos la API KEY desde el archivo .env
load_dotenv()
API_KEY = os.getenv("AEMET_API_KEY")
URL_AEMET = f"https://opendata.aemet.es/opendata/api/observacion/convencional/todas/?api_key={API_KEY}"

# 2. Configuración robusta del Productor
try:
    producer = KafkaProducer(
        bootstrap_servers=['127.0.0.1:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        # Esta línea evita el error "Invalid file object" al forzar la versión
        api_version=(0, 10, 1),
        # Reintentos por si Kafka está despertando
        retries=5
    )
except Exception as e:
    print(f"Error al conectar con Kafka: {e}")

def fetch_aemet_data():
    try:
        print(f"Consultando API de AEMET...")
        res = requests.get(URL_AEMET)
        res.raise_for_status() # Verifica si la API devolvió error (401, 404, etc)
        
        datos_url = res.json().get('datos')
        if not datos_url:
            print("No se recibió URL de datos. Revisa tu API KEY.")
            return

        # Obtener datos reales de la URL temporal que da AEMET
        data_res = requests.get(datos_url)
        observations = data_res.json()
        
        print(f"Recibidas {len(observations)} observaciones. Enviando a Kafka...")
        
        for obs in observations:
            producer.send('weather_raw', obs)
            # Solo imprimimos algunos para no colapsar la terminal
            if observations.index(obs) % 50 == 0:
                print(f"Progreso: Enviada estación {obs.get('idema')}")
            
        producer.flush()
        print("¡Lote enviado con éxito!")
        
    except Exception as e:
        print(f"Error durante la ejecución: {e}")

if __name__ == "__main__":
    while True:
        print("\n--- Iniciando ciclo de ingesta ---")
        fetch_aemet_data()
        # Cambiamos a 60 segundos para probar rápido hasta que entre
        print("Esperando 60 segundos para reintentar...")
        time.sleep(60)