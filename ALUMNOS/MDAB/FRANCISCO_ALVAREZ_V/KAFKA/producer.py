import os # Librería para manejar rutas y archivos en el sistema operativo
import json # Librería para trabajar con datos en formato JSON (aunque aquí no se usa directamente)
import time # Librería para manejar pausas y tiempos de espera
from confluent_kafka import Producer # Librería para producir mensajes en Apache Kafka

# Configuracion del productor Kafka
configuracion = {
    'bootstrap.servers': 'localhost:9092', # Dirección del servidor Kafka (cambiar si está en otra máquina)
    'client.id': 'producer-banco-miami'  # Identificador único para este productor
}

# Creamos el objeto productor usando la configuración anterior
productor = Producer(configuracion)


TOPIC = 'transacciones_banco_miami'

# Construimos la ruta completa del archivo "el_quijote_book.txt" usando la ubicación actual del script
ruta_archivo = os.path.join(os.path.dirname(__file__), 'transacciones.txt')

# Verificamos si el archivo existe en la ruta indicada
if not os.path.exists(ruta_archivo):
    # Si no existe, lanzamos un error indicando que no se encontró el archivo
    raise FileNotFoundError(f"No se encontro el archivo: {ruta_archivo}")

# Abrimos el archivo en modo lectura con codificación UTF-8 para soportar caracteres especiales como acentos y eñes, etc.
with open(ruta_archivo, encoding='utf-8') as archivo:
    lineas = archivo.readlines() # Leemos todas las líneas del archivo y las guardamos en una lista

print("  PRODUCER - BANCO MIAMI-VENEZUELA")
print(f"  Topic: {TOPIC}")
print(f"  Transacciones cargadas: {len(lineas)}")



for i, linea in enumerate(lineas):
    linea = linea.strip()
    if not linea:
        continue

   
    transaccion = json.loads(linea)

    print(f"  [{i+1}/{len(lineas)}] Enviando {transaccion['id_transaccion']}: "
          f"{transaccion['cliente_nombre']} | "
          f"${transaccion['monto']:,.2f} USD | "
          f"{transaccion['sucursal_origen']} -> {transaccion['sucursal_destino']}")

    # Enviamos la palabra al topic de Kafka, codificada en UTF-8, junto con su clave
    productor.produce(topic=TOPIC,key=transaccion['id_transaccion'].encode('utf-8'),value=json.dumps(transaccion, ensure_ascii=False).encode('utf-8'))
    
    productor.flush()

    
    time.sleep(1.5)


print(f"  COMPLETADO: {len(lineas)} transacciones enviadas al topic '{TOPIC}'")

