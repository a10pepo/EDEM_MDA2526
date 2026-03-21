import json
from kafka import KafkaConsumer, KafkaProducer

# Configuración del Consumer
consumer = KafkaConsumer(
    'weather_raw',
    bootstrap_servers=['127.0.0.1:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    api_version=(0, 10, 1) 
)

# Configuración del Producer
producer = KafkaProducer(
    bootstrap_servers=['127.0.0.1:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    api_version=(0, 10, 1)  
)

print("🚀 Procesador iniciado. Monitoreando alertas de frío (< 3°C)...")

try:
    for message in consumer:
        raw_data = message.value
        
        station_id = raw_data.get('idema')
        station_name = raw_data.get('ubi', 'Desconocida') # Nombre de la ciudad
        temp = raw_data.get('ta')
        
        if station_id and temp is not None:
            temp_float = float(temp)
            
            # 1. Creamos el mensaje base
            processed_msg = {
                "station_id": station_id,
                "station_name": station_name,
                "temp_c": temp_float,
                "wind_speed": raw_data.get('vv', 0),
                "timestamp": raw_data.get('fint'),
                "status": "NORMAL" 
            }
            
            # 2. Lógica de ALARMA (Menor de 3 grados)
            if temp_float < 3.0:
                processed_msg["status"] = "ALERTA_FRIO"
                # Printeo especial para la terminal
                print(f"❄️  ¡ALERTA DE FRÍO! Estación: {station_name} ({station_id}) -> {temp_float}°C")
            else:
                print(f"✅ Procesado: {station_id} -> {temp_float}°C")
            
            # 3. Enviamos a Kafka (tanto normales como alertas)
            producer.send('weather_processed', processed_msg)
            producer.flush() 
            
except KeyboardInterrupt:
    print("\nDeteniendo procesador...")
finally:
    consumer.close()