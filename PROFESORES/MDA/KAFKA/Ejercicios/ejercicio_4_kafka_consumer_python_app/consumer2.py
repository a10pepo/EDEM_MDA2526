from confluent_kafka import Consumer
import json  # <--- NUEVO 1: Importamos la librería para entender el formato de los datos

# ============================================
# CONFIGURACIÓN DEL CONSUMIDOR
# ============================================
config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo-consumidor-filtro', # He cambiado el nombre para que no choque con el anterior
    'auto.offset.reset': 'earliest' # 'earliest' para asegurar que leemos desde el principio si es nuevo
}

consumer = Consumer(config)
topic_kafka = 'alertas_stock' # Asegúrate de que este nombre coincide con el de tu productor (topicEdem o alertas_stock)
consumer.subscribe([topic_kafka])

print(f"Esperando mensajes FILTRADOS del tópico '{topic_kafka}'...")

# <--- NUEVO 2: Inicializamos el contador fuera del bucle
contador_aprobados = 0 

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print(f"Error al recibir mensaje: {msg.error()}")
            continue

        # ============================================
        # AQUÍ EMPIEZA LA LÓGICA NUEVA
        # ============================================
        
        # 1. Deserializar: Bytes -> Texto -> Diccionario Python
        mensaje_texto = msg.value().decode('utf-8')
        datos = json.loads(mensaje_texto) 
        
        # 2. Filtrar: ¿Contiene la clave 'Estado' y es igual a 'Aprobado'?
        # Usamos .get() por seguridad (si no existe la clave, no da error)
        if datos.get('Estado') == 'Aprobado':
            
            # 3. Contar: Aumentamos el contador
            contador_aprobados += 1
            
            # 4. Mostrar resultado
            print(f"[{contador_aprobados}] ¡Mensaje Aceptado! -> {datos}")
            
        # Si NO es 'Aprobado', el programa no hace nada y vuelve al inicio del bucle (ignora el mensaje)

except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario.")

finally:
    consumer.close()