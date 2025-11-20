from confluent_kafka import Producer
import json

BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC = 'transferencias'
TOPIC_PENDIENTES = 'transferencias_pendientes'

transferencias = [
    {"id_transferencia":"T001","fecha":"2024-11-21T10:15:00Z","cuenta_origen":"KY12345678901234567890","pais_origen":"Islas Caimán","cuenta_destino":"ES09876543210987654321","pais_destino":"España","monto":2500.75,"moneda":"EUR","concepto":"Pago de alquiler","estado":"Completada"},
    {"id_transferencia":"T002","fecha":"2024-11-21T12:30:00Z","cuenta_origen":"SG11223344556677889900","pais_origen":"Singapur","cuenta_destino":"US99887766554433221100","pais_destino":"Estados Unidos","monto":150.00,"moneda":"USD","concepto":"Compra en línea","estado":"Completada"},
    {"id_transferencia":"T003","fecha":"2024-11-22T08:45:00Z","cuenta_origen":"FR12345678901234567890","pais_origen":"Francia","cuenta_destino":"GB12345678901234567890","pais_destino":"Reino Unido","monto":5000.00,"moneda":"EUR","concepto":"Transferencia empresarial","estado":"Pendiente"},
    {"id_transferencia":"T004","fecha":"2024-11-22T14:00:00Z","cuenta_origen":"DE22334455667788990011","pais_origen":"Alemania","cuenta_destino":"IT12345678901234567890","pais_destino":"Italia","monto":750.25,"moneda":"EUR","concepto":"Pago de proveedores","estado":"Completada"},
    {"id_transferencia":"T005","fecha":"2024-11-23T09:20:00Z","cuenta_origen":"US99887766554433221100","pais_origen":"Estados Unidos","cuenta_destino":"ES11223344556677889900","pais_destino":"España","monto":500.00,"moneda":"USD","concepto":"Compra de tecnología","estado":"Completada"},
    {"id_transferencia":"T006","fecha":"2024-11-23T11:00:00Z","cuenta_origen":"KY11223344556677889900","pais_origen":"Islas Caimán","cuenta_destino":"ES55667788990011223344","pais_destino":"España","monto":1250.00,"moneda":"EUR","concepto":"Pago de dividendos","estado":"Completada"}
]

producer = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})

for tranferencia in transferencias:
    mensaje = json.dumps(tranferencia, ensure_ascii=False).encode('utf-8')
    print(f'Enviado tranferencia {tranferencia}')
    producer.produce(TOPIC, value=mensaje)
    if tranferencia['estado'] == 'Pendiente':
        producer.produce(TOPIC_PENDIENTES, value=mensaje)

producer.flush()
print("Datos enviados a Kafka")