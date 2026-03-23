from confluent_kafka import Consumer
import json

config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'vip-monitor-group',
    'auto.offset.reset': 'latest' # Solo ver lo nuevo
}

consumer = Consumer(config)
topic_final = 'vip_large_transactions' # Este tópico lo creó KSQL

consumer.subscribe([topic_final])

print(f"MONITOR VIP ACTIVO: Escuchando '{topic_final}'...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        
        # KSQL a veces envía los datos en mayúsculas dependiendo de la config, 
        # pero el JSON es estándar.
        val = msg.value().decode('utf-8')
        data = json.loads(val)
        
        print(f"ALERTA: VENTA GRANDE DETECTADA")
        print(f"   Cliente: {data.get('USER') or data.get('user')}") # KSQL a veces pone keys en mayusculas
        print(f"   Monto:   ${data.get('AMOUNT') or data.get('amount')}")
        print(f"   Tarjeta: {data.get('CARD') or data.get('card')}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()