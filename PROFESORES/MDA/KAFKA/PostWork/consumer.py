from confluent_kafka import Consumer, Producer, KafkaError
import json

RAW_TOPIC = "raw_weather"
ALERT_TOPIC = "weather_alerts"

# =======================
# CONFIGURACIÓN DEL CONSUMIDOR
# =======================
consumer_conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "weather_processor_group",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(consumer_conf)
consumer.subscribe([RAW_TOPIC])

# =======================
# CONFIGURACIÓN DEL PRODUCTOR
# =======================
producer = Producer({"bootstrap.servers": "localhost:9092"})

print("Consumer intermedio iniciado...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Error del consumidor:", msg.error())
            continue

        try:
            # Decodificar mensaje JSON
            data = json.loads(msg.value().decode("utf-8"))
            print("Mensaje recibido:", data)

            tmax = data.get("tamax")
            tmin = data.get("tamin")
            estacion = data.get("ubi", "desconocida")

            # ---- FILTRO DE OLA DE FRÍO ----
            if tmax is not None and tmin is not None:
                if tmax < 3 and tmin < 0:
                    # Crear alerta incluyendo todos los datos originales
                    alerta = data.copy()
                    alerta["mensaje"] = f"⚠️ Ola de frío: {tmax}°C, min {tmin}°C"

                    # Enviar alerta a Kafka
                    producer.produce(ALERT_TOPIC, value=json.dumps(alerta))
                    producer.flush()
                    print("➡️ ALERTA enviada:", alerta)

        except json.JSONDecodeError:
            print("⚠️ Error: mensaje recibido no es JSON válido")
        except Exception as e:
            print(f"⚠️ Error procesando mensaje: {e}")

except KeyboardInterrupt:
    print("Deteniendo consumer intermedio...")
finally:
    consumer.close()
