import os  # Librería para manejar rutas y archivos en el sistema operativo
import json  # Librería para trabajar con datos en formato JSON (aunque aquí no se usa directamente)
import time  # Librería para manejar pausas y tiempos de espera
import re  # Librería para trabajar con expresiones regulares (para separar palabras)
from confluent_kafka import Producer  # Librería para producir mensajes en Apache Kafka

# Configuración del productor de Kafka: aquí indicamos dónde está el servidor y el identificador del cliente
configuracion = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del servidor Kafka (cambiar si está en otra máquina)
    'client.id': 'productor-python'  # Identificador único para este productor
}

# Creamos el objeto productor usando la configuración anterior
productor = Producer(configuracion)

# Nombre del tema (topic) en Kafka donde se enviarán las palabras
topic_kafka = 'palabras'

# Construimos la ruta completa del archivo "el_quijote_book.txt" usando la ubicación actual del script
ruta_archivo = os.path.join(os.path.dirname(__file__), 'el_quijote_book.txt')

# Verificamos si el archivo existe en la ruta indicada
if not os.path.exists(ruta_archivo):
    # Si no existe, lanzamos un error indicando que no se encontró el archivo
    raise FileNotFoundError(f"El archivo no se encuentra en la ruta: {ruta_archivo}")

# Abrimos el archivo en modo lectura con codificación UTF-8 para soportar caracteres especiales como acentos y eñes, etc.
with open(ruta_archivo, encoding="utf8") as archivo:
    lineas = archivo.readlines()  # Leemos todas las líneas del archivo y las guardamos en una lista

contador = 0  # Inicializamos un contador para asignar una clave única a cada palabra enviada

# Recorremos cada línea del archivo
for linea in lineas:
    time.sleep(2)  # Esperamos 2 segundos antes de procesar la siguiente línea (simulación de envío pausado)
    print(linea.strip() )  # Mostramos la línea en pantalla, eliminando espacios extra al principio y final de linea, y quitamos los retornos de linea.

    # Usamos una expresión regular para separar las palabras y signos de puntuación
    palabras = re.findall(r"[\w']+|[.,!?;]", linea)

    # Recorremos cada palabra encontrada en la línea
    for palabra in palabras:
        clave = str(contador)  # Convertimos el contador en texto para usarlo como clave

        # Enviamos la palabra al topic de Kafka, codificada en UTF-8, junto con su clave
        productor.produce(topic=topic_kafka, value=palabra.encode('utf-8'), key=clave)

        contador += 1  # Incrementamos el contador para la siguiente palabra

# Esperamos a que todos los mensajes pendientes se envíen antes de terminar
productor.flush()

# Mostramos un mensaje indicando que todo se envió correctamente
print("Todos los mensajes del libro El Quijote han sido enviados correctamente.")
