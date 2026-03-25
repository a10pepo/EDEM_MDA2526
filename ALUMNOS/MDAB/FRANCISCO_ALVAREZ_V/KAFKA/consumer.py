import json
from confluent_kafka import Consumer

# Configuracion del consumidor Kafka
configuracion = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo-banco-miami',
    'auto.offset.reset': 'earliest'
}

# Creamos el consumidor con la configuración anterior
consumidor = Consumer(configuracion)

# Topic de donde se leen las transacciones
TOPIC = 'transacciones_banco_miami'

print("  CONSUMER - BANCO MIAMI-VENEZUELA")
print(f"  Topic: {TOPIC}")
print("  Esperando transacciones...")

consumidor.subscribe([TOPIC]) # Nos suscribimos al topic para empezar a recibir mensajes / suscribe al consumidor a uno o más topics de Kafka para que empiece a recibir mensajes de ellos.

contador = 0

try:
    while True:
        msg = consumidor.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"  Error: {msg.error()}")
            continue

        datos = json.loads(msg.value().decode('utf-8'))

        contador += 1

        if datos['monto'] > 10000:
            print("  *** ALERTA: Transacción de alto valor detectada! ***")

            print(f"  --- Transaccion #{contador} ---")
            print(f"  ID:          {datos['id_transaccion']}")
            print(f"  Fecha:       {datos['fecha']}")
            print(f"  Cliente:     {datos['cliente_nombre']} ({datos['cliente_id']})")
            print(f"  Monto:       ${datos['monto']:,.2f} USD")
            print(f"  Tipo:        {datos['tipo_operacion']}")
            print(f"  Origen:      {datos['sucursal_origen']} ({datos['pais_origen']})")
            print(f"  Destino:     {datos['sucursal_destino']} ({datos['pais_destino']})")
            print(f"  Estado:      {datos['estado']}")

except KeyboardInterrupt:
    print()
    print(f"  Finalizado - Total transacciones recibidas: {contador}")

finally:
    consumidor.close()
