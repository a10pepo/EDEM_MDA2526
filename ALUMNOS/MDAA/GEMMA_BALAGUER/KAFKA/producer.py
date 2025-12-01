import requests
import json
from confluent_kafka import Producer
import time

# =======================
# CONFIGURACIÓN DE LA API
# =======================
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJnYmFsYWd1ZXJhZGVsbEBnbWFpbC5jb20iLCJqdGkiOiIwM2RhNGE3Mi05NGM3LTQyNDMtODUwMC00MjA1ZjdkZTI2MWEiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc2NDUyMzI3NywidXNlcklkIjoiMDNkYTRhNzItOTRjNy00MjQzLTg1MDAtNDIwNWY3ZGUyNjFhIiwicm9sZSI6IiJ9.taxd2E3Z42ljuYEi-U0tsBfHSuwl0cxiTLpMDg0vmso"
URL = f"https://opendata.aemet.es/opendata/api/observacion/convencional/todas/?api_key={API_KEY}"

# =======================
# CONFIGURACIÓN DE KAFKA
# =======================
RAW_TOPIC = "raw_weather"
producer = Producer({"bootstrap.servers": "localhost:9092"})

def delivery_report(err, msg):
    if err:
        print("❌ Error enviando mensaje:", err)
    else:
        print(f"✅ Mensaje enviado a {msg.topic()} [{msg.partition()}]")

print("Producer AEMET iniciado...")

# =======================
# BUCLE PRINCIPAL
# =======================
while True:
    try:
        # Obtener URL de los datos
        r = requests.get(URL, timeout=10)
        try:
            info = r.json()
        except json.JSONDecodeError:
            print("⚠ La API devolvió texto no JSON:")
            print(r.text[:500])
            time.sleep(120)
            continue

        # Validar estado de la API
        if info.get("estado") != 200:
            print(f"⚠ API devolvió estado {info.get('estado')}: {info.get('descripcion')}")
            time.sleep(60)
            continue

        datos_url = info.get("datos")
        if not datos_url:
            print("⚠ No se encontró 'datos' en la respuesta.")
            time.sleep(60)
            continue

        # Descargar los datos reales
        resp = requests.get(datos_url, timeout=10)
        try:
            data = resp.json()
        except json.JSONDecodeError:
            print("⚠ Error: datos_url NO devolvió JSON válido")
            print(resp.text[:500])
            time.sleep(60)
            continue

        print(f"✓ Datos descargados: {len(data)} registros")

        # Enviar cada registro completo a Kafka
        for item in data:
            try:
                # Mostrar JSON completo antes de enviarlo
                print("Enviando mensaje a Kafka:", json.dumps(item, indent=2))
                producer.produce(RAW_TOPIC, value=json.dumps(item), callback=delivery_report)
            except Exception as e:
                print("❌ Error produciendo mensaje:", e)

        # Vaciar buffer de Kafka
        producer.flush()

        # Esperar antes de la siguiente consulta
        time.sleep(60)

    except Exception as e:
        print("⚠ Error al obtener datos de AEMET:", e)
        time.sleep(60)