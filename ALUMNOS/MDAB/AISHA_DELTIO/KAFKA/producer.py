import time
import csv
from json import dumps
from confluent_kafka import Producer

config = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'producer-strava'
}
producer = Producer(config)

topic_kafka = 'datos_strava'
archivo_csv = "jesus-activities.csv"

try:
    # Abrimos el archivo CSV
    with open(archivo_csv, mode='r', encoding='utf-8') as file:
        # DictReader convierte cada fila automáticamente en un diccionario JSON
        reader = csv.DictReader(file)

        for fila in reader:
            data_str = dumps(fila, ensure_ascii=False)
            data_bytes = data_str.encode('utf-8')
            producer.produce(topic=topic_kafka, value=data_bytes)
            time.sleep(1) 

    # Esperamos a que se envíen los mensajes pendientes
    pending = producer.flush()

    if pending == 0:
        print("\n--- Todos los mensajes entregados correctamente ---")
    else:
        print(f"\n{pending} mensajes no se pudieron entregar.")

except FileNotFoundError:
    print(f"ERROR: No encuentro el archivo '{archivo_csv}'.")