# IMPORTACIÓN DE LIBRERÍAS
import time                             # Librería para manejar pausas y tiempos de espera
from json import dumps
from confluent_kafka import Producer    # Librería para producir mensajes en Apache Kafka
import os                               # Librería para manejar rutas y archivos en el sistema operativo


# CONFIGURACIÓN DEL PRODUCTOR
config = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'python-producer'
}

producer = Producer(config)


# DEFINICIÓN DEL TÓPICO
topic_kafka = 'laliga_players'


# ENVÍO DE MENSAJES
# Construimos la ruta completa del archivo "laliga_players.txt" usando la ubicación actual del script
file_path = os.path.join(os.path.dirname(__file__), 'laliga_players.txt')

# Verificamos si el archivo existe en la ruta indicada
if not os.path.exists(file_path):
    # Si no existe, lanzamos un error indicando que no se encontró el archivo
    raise FileNotFoundError(f"El archivo no se encuentra en la ruta: {file_path}")

# Abrimos el archivo en modo lectura con codificación UTF-8 para soportar caracteres especiales como acentos y eñes, etc.
with open(file_path, encoding="utf8") as file:
    file_lines = file.readlines()  # Leemos todas las líneas del archivo y las guardamos en una lista

print(f"Archivo '{file_path}' de tipo {type(file_lines)} leído correctamente. Total de líneas: {len(file_lines)}")


counter = 0  # Inicializamos un contador para asignar una clave única a cada palabra enviada

for line in file_lines:
    time.sleep(2)  # Esperamos 2 segundos antes de procesar la siguiente línea (simulación de envío pausado)
    print(f"Enviando datos al tópico {topic_kafka}: {line.strip()}")  # Mostramos la línea en pantalla, eliminando espacios extra
    
    line_bytes = line.encode('utf-8')  # Convertimos la línea a bytes para Kafka
    
    # Enviamos la línea al topic de Kafka, codificada en UTF-8, junto con su clave
    producer.produce(topic=topic_kafka, value=line_bytes, key=str(counter))

    counter += 1  # Incrementamos el contador para la siguiente palabra


# FLUSH FINAL

# Comprobamos si hubo mensajes que no se pudieron entregar.
pending = producer.flush()
if pending != 0:
    print(f"{pending} mensajes no se pudieron entregar.")


# Esperamos a que todos los mensajes pendientes se envíen antes de terminar


print("Todos los mensajes del archivo 'laliga_players.txt' han sido enviados correctamente.")

