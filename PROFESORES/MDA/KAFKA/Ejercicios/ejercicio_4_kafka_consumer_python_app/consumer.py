from confluent_kafka import Consumer

# ============================================
# CONFIGURACIÓN DEL CONSUMIDOR
# ============================================
config = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del broker Kafka (como la IP de un servicio web)
    'group.id': 'grupo-consumidor',         # Identificador del grupo de consumidores
    'auto.offset.reset': 'earliest'         # Leer desde el principio si no hay posición guardada
}

# Creamos el consumidor con la configuración anterior
consumer = Consumer(config)

# Nos suscribimos al tópico que queremos leer
topic_kafka = 'proyectos_innovacion'
consumer.subscribe([topic_kafka])

print(f"Esperando mensajes del tópico '{topic_kafka}'...")

# ============================================
# try:
#   Significa "intenta ejecutar este bloque de código".
#   Si todo va bien, el código dentro de try se ejecuta normalmente.
#   Si ocurre un error o el usuario interrumpe el programa, pasamos a except o finally.
# ============================================
try:
    # ============================================
    # while True:
    #   Es un bucle infinito: se repite una y otra vez sin parar.
    #   ¿Por qué usamos esto? Porque queremos que el consumidor siga leyendo mensajes
    #   mientras el programa esté activo.
    # ============================================
    while True:
        # ============================================
        # consumer.poll(1.0):
        #   Intenta obtener un mensaje durante 1 segundo.
        #   Si llega un mensaje en ese tiempo, lo devuelve.
        #   Si no llega nada, devuelve None.
        # ¿Por qué 1 segundo?
        #   - Es un buen equilibrio: no bloquea demasiado tiempo y no consume recursos en exceso.
        # ============================================
        msg = consumer.poll(1.0)

        if msg is None:
            # No hay mensaje disponible en este momento, seguimos esperando
            continue

        if msg.error():
            # Si hay un error en el mensaje, lo mostramos
            print(f"Error al recibir mensaje: {msg.error()}")
            continue

        # Si el mensaje es válido, mostramos su contenido
        # msg.value() devuelve los datos en bytes, por eso usamos decode('utf-8') para convertirlos a texto
        print(f"Mensaje recibido: {msg.value().decode('utf-8')}")

# ============================================
# except:
#   Se ejecuta si ocurre una excepción (error) o si el usuario interrumpe el programa (Ctrl+C).
#   Aquí mostramos un mensaje para indicar que el programa se detuvo.
# ============================================
except KeyboardInterrupt:
    print("Programa detenido por el usuario.")

# ============================================
# finally:
#   Este bloque se ejecuta SIEMPRE, ocurra o no un error.
#   Aquí cerramos el consumidor para liberar recursos.
# ============================================
finally:
    consumer.close()