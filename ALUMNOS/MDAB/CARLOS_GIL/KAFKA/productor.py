import json
import time
import csv
from kafka import KafkaProducer

# Configuración del Productor
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Leyendo el dataset y enviando ventas a Kafka")

try:
    # Abrimos tu archivo CSV
    with open('datos_ventas.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convertimos el precio a entero para que no haya líos luego
            row['precio'] = int(row['precio'])
            
            # Enviamos al topic 'compras_raw'
            producer.send('compras_raw', value=row)
            
            print(f"Venta enviada: {row['cliente']} -> {row['modelo']} ({row['precio']}€)")
            time.sleep(2) # Pausa de 2 segundos para que lo veas fluir

    print("🏁 ¡Todos los datos del CSV han sido enviados!")

except FileNotFoundError:
    print("Error: No encuentro el archivo 'datos_ventas.csv'. Asegúrate de que está en la misma carpeta.")
except Exception as e:
    print(f"Ha ocurrido un error: {e}")
finally:
    producer.close()