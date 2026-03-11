import json
from kafka import KafkaConsumer, KafkaProducer

# Configuración del consumidor
consumer = KafkaConsumer(
    "fake_data",
    bootstrap_servers="127.0.0.1:9092",
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='my-sensor-group',
    # Eliminamos el deserializador de aquí para manejar errores manualmente
    value_deserializer=lambda x: x.decode('utf-8') 
)

# Configuración del productor
producer = KafkaProducer(
    bootstrap_servers="127.0.0.1:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)



print("Escuchando mensajes en 'fake_data'...")
print("-" * 50)

try:
    for message in consumer:
        try:
            # Deserialización manual para evitar que el script muera por un mensaje corrupto
            data = json.loads(message.value)
            
            if data.get("status") == "FAIL":
                # Enviamos al topic de alertas
                producer.send("SENSOR_FAILURES_2", data)
                
                print(f"ALERTA | Sensor: {data.get('sensor_id')} | "
                      f"Temp: {data.get('temperature')}°C | "
                      f"Status: {data.get('status')}")
        
        except json.JSONDecodeError:
            print(f"Error: Mensaje malformado recibido: {message.value}")

except KeyboardInterrupt:
    print("\nDeteniendo procesos...")
finally:
    # Cerramos ambos de forma limpia
    consumer.close()
    producer.flush() # Asegura que los mensajes pendientes se envíen
    producer.close()
    print("Conexiones cerradas.")