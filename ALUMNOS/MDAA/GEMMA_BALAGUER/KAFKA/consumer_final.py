from confluent_kafka import Consumer, KafkaError
import json

# Configuración del consumidor
consumer_conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "final_consumer_group",
    "auto.offset.reset": "earliest"  # Leer desde el inicio si no hay offsets
}

consumer = Consumer(consumer_conf)
consumer.subscribe(["weather_alerts"])

print("Consumer de alertas iniciado...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            # Ignorar fin de partición, mostrar otros errores
            if msg.error().code() != KafkaError._PARTITION_EOF:
                print("Error del consumidor:", msg.error())
            continue

        try:
            # Decodificar y parsear JSON
            alerta = json.loads(msg.value().decode("utf-8"))

            # Leer claves de forma segura, con valores por defecto
            estacion = alerta.get("ubi", "desconocida")
            tmax = alerta.get("tamax", "None")
            tmin = alerta.get("tamin", "None")
            mensaje = alerta.get("mensaje", "Sin mensaje")

            # Mostrar alerta de manera clara
            print("🚨 ALERTA DE TEMPERATURA 🚨")
            print(f"Estación: {estacion}")
            print(f"Temperatura máxima: {tmax}°C")
            print(f"Temperatura mínima: {tmin}°C")
            print(f"Mensaje: {mensaje}")
            print("-" * 50)

        except json.JSONDecodeError:
            print("⚠️ Error: Mensaje recibido no es JSON válido")
        except Exception as e:
            print(f"⚠️ Error procesando alerta: {e}")

except KeyboardInterrupt:
    print("Deteniendo consumidor de alertas...")
finally:
    consumer.close()