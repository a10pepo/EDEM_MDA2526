from kafka import KafkaConsumer, KafkaProducer
import json
import datetime

# Configuración del Consumidor (Lee datos crudos)
consumer = KafkaConsumer(
    'traffic_raw',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest', # Lee solo los mensajes nuevos desde que arranca
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Configuración del Productor (Escribe datos procesados)
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

SOURCE_TOPIC = 'traffic_raw'
TARGET_TOPIC = 'traffic_speeding'
SPEED_LIMIT = 120

print(f"👮 Iniciando radar de velocidad.")
print(f"Escuchando '{SOURCE_TOPIC}' y enviando infracciones a '{TARGET_TOPIC}'...")

try:
    for message in consumer:
        data = message.value
        
        # Lógica de negocio: Filtrar solo excesos de velocidad
        if data['speed'] > SPEED_LIMIT:
            # Enriquecimiento: Calcular severidad
            if data['speed'] > 150:
                severity = "CRITICAL"
            elif data['speed'] > 135:
                severity = "HIGH"
            else:
                severity = "MODERATE"
            
            # Crear nuevo mensaje transformado
            transformed_data = {
                "sensor_id": data['sensor_id'],
                "vehicle_plate": data['vehicle_plate'],
                "speed": data['speed'],
                "severity": severity,
                "processed_at": datetime.datetime.now().isoformat()
            }
            
            # Enviar al topic de infracciones
            producer.send(TARGET_TOPIC, value=transformed_data)
            
            print(f"🚨 INFRACCIÓN DETECTADA: {transformed_data['vehicle_plate']} a {transformed_data['speed']}km/h ({severity})")
            
except KeyboardInterrupt:
    print("\nDeteniendo procesador...")