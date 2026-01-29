# IMPORT LIBRARIES
import time             # sleep
from json import dumps  # convert dictionaries to json strings.
# (pip install confluent-kafka --- must be already installed) (both python and pip properly installed)
from confluent_kafka import Producer    # connect to Kafka and send messages

# Meto en python el fichero de datos
transferencias = [
    {"id_transferencia":"T001","fecha":"2024-11-21T10:15:00Z","cuenta_origen":"KY12345678901234567890","pais_origen":"Islas Caimán","cuenta_destino":"ES09876543210987654321","pais_destino":"España","monto":2500.75,"moneda":"EUR","concepto":"Pago de alquiler","estado":"Completada"},
    {"id_transferencia":"T002","fecha":"2024-11-21T12:30:00Z","cuenta_origen":"SG11223344556677889900","pais_origen":"Singapur","cuenta_destino":"US99887766554433221100","pais_destino":"Estados Unidos","monto":150.00,"moneda":"USD","concepto":"Compra en línea","estado":"Completada"},
    {"id_transferencia":"T003","fecha":"2024-11-22T08:45:00Z","cuenta_origen":"FR12345678901234567890","pais_origen":"Francia","cuenta_destino":"GB12345678901234567890","pais_destino":"Reino Unido","monto":5000.00,"moneda":"EUR","concepto":"Transferencia empresarial","estado":"Pendiente"},
    {"id_transferencia":"T004","fecha":"2024-11-22T14:00:00Z","cuenta_origen":"DE22334455667788990011","pais_origen":"Alemania","cuenta_destino":"IT12345678901234567890","pais_destino":"Italia","monto":750.25,"moneda":"EUR","concepto":"Pago de proveedores","estado":"Completada"},
    {"id_transferencia":"T005","fecha":"2024-11-23T09:20:00Z","cuenta_origen":"US99887766554433221100","pais_origen":"Estados Unidos","cuenta_destino":"ES11223344556677889900","pais_destino":"España","monto":500.00,"moneda":"USD","concepto":"Compra de tecnología","estado":"Completada"},
    {"id_transferencia":"T006","fecha":"2024-11-23T11:00:00Z","cuenta_origen":"KY11223344556677889900","pais_origen":"Islas Caimán","cuenta_destino":"ES55667788990011223344","pais_destino":"España","monto":1250.00,"moneda":"EUR","concepto":"Pago de dividendos","estado":"Completada"},
    {"id_transferencia":"T007","fecha":"2024-11-24T16:10:00Z","cuenta_origen":"SG22334455667788990011","pais_origen":"Singapur","cuenta_destino":"DE99887766554433221100","pais_destino":"Alemania","monto":350.00,"moneda":"EUR","concepto":"Transferencia comercial","estado":"Pendiente"},
    {"id_transferencia":"T008","fecha":"2024-11-24T18:00:00Z","cuenta_origen":"DE33445566778899001122","pais_origen":"Alemania","cuenta_destino":"IT12345678901234567890","pais_destino":"Italia","monto":4000.75,"moneda":"USD","concepto":"Pago de contrato","estado":"Completada"},
    {"id_transferencia":"T009","fecha":"2024-11-25T13:30:00Z","cuenta_origen":"SG99887766554433221100","pais_origen":"Singapur","cuenta_destino":"US22334455667788990011","pais_destino":"Estados Unidos","monto":750.50,"moneda":"USD","concepto":"Compra de acciones","estado":"Completada"},
    {"id_transferencia":"T010","fecha":"2024-11-25T15:45:00Z","cuenta_origen":"KY55667788990011223344","pais_origen":"Islas Caimán","cuenta_destino":"IT44556677889900112233","pais_destino":"Italia","monto":2000.00,"moneda":"EUR","concepto":"Pago por consultoría","estado":"Completada"},
    {"id_transferencia":"T011","fecha":"2024-11-26T08:10:00Z","cuenta_origen":"SG55667788990011223344","pais_origen":"Singapur","cuenta_destino":"GB33445566778899001122","pais_destino":"Reino Unido","monto":1000.00,"moneda":"GBP","concepto":"Préstamo personal","estado":"Completada"},
    {"id_transferencia":"T012","fecha":"2024-11-26T11:45:00Z","cuenta_origen":"DE66778899001122334455","pais_origen":"Alemania","cuenta_destino":"ES55667788990011223344","pais_destino":"España","monto":300.00,"moneda":"EUR","concepto":"Pago de factura","estado":"Completada"},
    {"id_transferencia":"T013","fecha":"2024-11-27T09:25:00Z","cuenta_origen":"US22334455667788990011","pais_origen":"Estados Unidos","cuenta_destino":"GB22334455667788990011","pais_destino":"Reino Unido","monto":1500.50,"moneda":"GBP","concepto":"Inversión inmobiliaria","estado":"Completada"},
    {"id_transferencia":"T014","fecha":"2024-11-27T14:00:00Z","cuenta_origen":"SG22334455667788990011","pais_origen":"Singapur","cuenta_destino":"IT66778899001122334455","pais_destino":"Italia","monto":850.00,"moneda":"EUR","concepto":"Pago por servicios legales","estado":"Completada"},
    {"id_transferencia":"T015","fecha":"2024-11-28T08:30:00Z","cuenta_origen":"FR11223344556677889900","pais_origen":"Francia","cuenta_destino":"ES66778899001122334455","pais_destino":"España","monto":1250.50,"moneda":"EUR","concepto":"Pago por software","estado":"Completada"},
    {"id_transferencia":"T016","fecha":"2024-11-28T11:00:00Z","cuenta_origen":"US33445566778899001122","pais_origen":"Estados Unidos","cuenta_destino":"FR66778899001122334455","pais_destino":"Francia","monto":4500.00,"moneda":"USD","concepto":"Venta de propiedad","estado":"Pendiente"},
    {"id_transferencia":"T017","fecha":"2024-11-29T10:15:00Z","cuenta_origen":"US22334455667788990011","pais_origen":"Estados Unidos","cuenta_destino":"GB55667788990011223344","pais_destino":"Reino Unido","monto":3200.00,"moneda":"GBP","concepto":"Transferencia de fondos","estado":"Completada"},
    {"id_transferencia":"T018","fecha":"2024-11-29T12:40:00Z","cuenta_origen":"IT22334455667788990011","pais_origen":"Italia","cuenta_destino":"DE55667788990011223344","pais_destino":"Alemania","monto":800.75,"moneda":"EUR","concepto":"Pago de proveedores","estado":"Completada"},
    {"id_transferencia":"T019","fecha":"2024-11-30T14:15:00Z","cuenta_origen":"US22334455667788990011","pais_origen":"Estados Unidos","cuenta_destino":"ES22334455667788990011","pais_destino":"España","monto":950.25,"moneda":"USD","concepto":"Pago de inversión","estado":"Completada"},
    {"id_transferencia":"T020","fecha":"2024-11-30T17:20:00Z","cuenta_origen":"SG33445566778899001122","pais_origen":"Singapur","cuenta_destino":"IT33445566778899001122","pais_destino":"Italia","monto":720.00,"moneda":"EUR","concepto":"Pago de salario","estado":"Completada"},
    {"id_transferencia":"T021","fecha":"2024-12-01T10:00:00Z","cuenta_origen":"KY11223344556677889900","pais_origen":"Islas Caimán","cuenta_destino":"IT11223344556677889900","pais_destino":"Italia","monto":1500.00,"moneda":"EUR","concepto":"Donación","estado":"Completada"}
]

# PRODUCER CONFIGURATION
config = {
    'bootstrap.servers': 'localhost:9092',  # - bootstrap.servers: Kafka server path
    'client.id': 'python-producer'          # - client.id: name to identify this programm (producer). it helps to know who is sending data when there are a lot of clients.
}


# Create producer with config ^^    (Producer is the component which sends messages to Kafka)
producer = Producer(config)


# TOPIC DEFINITION
topic_kafka = 'bank_transfers'  # a topic is the "channel" where messages are published by.


# SEND MESSAGES
for e in range(len(transferencias)):      
    data = {                                            # Create a dictionary with the data
        "id_transferencia": transferencias[e]["id_transferencia"],
        "fecha": transferencias[e]["fecha"],
        "cuenta_origen": transferencias[e]["cuenta_origen"],
        "pais_origen": transferencias[e]["pais_origen"],
        "cuenta_destino": transferencias[e]["cuenta_destino"],
        "pais_destino": transferencias[e]["pais_destino"],
        "monto": transferencias[e]["monto"],
        "moneda": transferencias[e]["moneda"],
        "concepto": transferencias[e]["concepto"],
        "estado": transferencias[e]["estado"]
    }           # each message is text with info about the transfers.

    # Convertimos el diccionario a una cadena JSON (texto estructurado).
    # dumps() transforma un objeto Python (dict) en texto JSON (str)
    # Por defecto, JSON convierte caracteres especiales (como á, ñ, ó) a códigos Unicode (\uXXXX)
    # porque intenta usar solo ASCII (un estándar antiguo que solo incluye letras inglesas).
    # Al poner ensure_ascii=False, mantenemos los acentos y caracteres tal cual.
    data_str = dumps(data, ensure_ascii=False)

    # Convertimos la cadena a bytes porque Kafka trabaja con datos binarios.
    # ¿Por qué binario? Porque es el formato estándar para enviar datos por la red.
    # encode('utf-8') transforma texto (str) en bytes (binario)
    data_bytes = data_str.encode('utf-8')

    # Enviamos el mensaje al tópico definido.
    # IMPORTANTE: produce() es ASÍNCRONO.
    # Esto significa que el mensaje no se envía inmediatamente,
    # sino que se guarda en un buffer interno y se envía en segundo plano.
    producer.produce(topic=topic_kafka, value=data_bytes)

    # Mostramos en pantalla lo que estamos enviando.
    print(f"Enviando datos: {data} al tópico {topic_kafka}")

    # Pausa de 1 segundo entre mensajes para simular un flujo en tiempo real.
    time.sleep(1)


# ============================================
# FLUSH FINAL
# ============================================
# ¿Por qué usamos flush()?
# Como produce() es asíncrono, algunos mensajes pueden quedar en el buffer
# cuando el programa termina. flush() espera a que TODOS los mensajes pendientes
# se envíen al broker antes de cerrar el programa.
pending = producer.flush()
# Comprobamos si hubo mensajes que no se pudieron entregar.
# flush() devuelve el número de mensajes que no se enviaron.
if pending != 0:
    print(f"{pending} mensajes no se pudieron entregar.")