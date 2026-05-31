import json
from confluent_kafka import Consumer, Producer

# ==========================================
# 1. CONFIGURACIÓN
# ==========================================
BROKER_URL = 'localhost:9092'
SOURCE_TOPIC = 'raw-transactions'          # De donde leemos
TARGET_TOPIC = 'standardized-transactions' # A donde escribimos

# Configuración del Consumer (Lectura)
consumer_conf = {
    'bootstrap.servers': BROKER_URL,
    'group.id': 'fintech-processor-group-v1', # Importante para no repetir mensajes
    'auto.offset.reset': 'earliest'           # Leer desde el principio si es nuevo
}

# Configuración del Producer (Escritura)
producer_conf = {
    'bootstrap.servers': BROKER_URL,
    'client.id': 'fintech-processor-writer'
}

consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)

# Tasas de cambio fijas (Mock)
EXCHANGE_RATES = {
    'USD': 0.92,  # 1 USD = 0.92 EUR
    'GBP': 1.15,  # 1 GBP = 1.15 EUR
    'EUR': 1.0    # 1 EUR = 1.0 EUR
}

# ==========================================
# 2. LÓGICA DE PROCESAMIENTO
# ==========================================
def process_message(msg_value):
    """
    Recibe un JSON string, lo convierte a dict,
    filtra y transforma los datos.
    Retorna el dict modificado o None si se filtra.
    """
    data = json.loads(msg_value)

    # A) FILTRO: Si es FAILED, lo descartamos
    if data.get('status') == 'FAILED':
        print(f"🚫 FILTRADO (FAILED): Tx {data['transaction_id']}")
        return None

    # B) TRANSFORMACIÓN: Convertir moneda
    curr = data['currency']
    amount = data['amount']

    if curr in EXCHANGE_RATES:
        # Calculamos el nuevo valor en EUR
        new_amount = round(amount * EXCHANGE_RATES[curr], 2)
        
        # Enriquecemos el JSON
        data['original_amount'] = amount
        data['original_currency'] = curr
        data['amount'] = new_amount      # Sobreescribimos con el valor en EUR
        data['currency'] = 'EUR'         # Ahora todo es EUR
        data['processed_by'] = 'python-consumer'
        
        return data
    
    return data # Si es otra moneda no contemplada (no debería pasar)

# ==========================================
# 3. BUCLE PRINCIPAL
# ==========================================
if __name__ == '__main__':
    consumer.subscribe([SOURCE_TOPIC])
    print(f"🔄 Iniciando Processor: Leemos de '{SOURCE_TOPIC}' -> Escribimos en '{TARGET_TOPIC}'")
    print("-------------------------------------------------------------------------------")

    try:
        while True:
            # 1. Leer mensaje (timeout de 1s para no bloquear)
            msg = consumer.poll(1.0)

            if msg is None: continue
            if msg.error():
                print(f"Error Consumer: {msg.error()}")
                continue

            # 2. Procesar
            val_str = msg.value().decode('utf-8')
            clean_data = process_message(val_str)

            # 3. Si hay datos limpios (no fue filtrado), enviamos al siguiente topic
            if clean_data:
                # Serializar de nuevo a JSON
                clean_json = json.dumps(clean_data)
                
                # Enviar al Topic de destino
                producer.produce(TARGET_TOPIC, value=clean_json.encode('utf-8'))
                
                # Log visual para tu captura de pantalla
                print(f"✅ PROCESADO: {clean_data['original_amount']} {clean_data['original_currency']} "
                    f"---> {clean_data['amount']} EUR")
                
                # Forzamos envío para ver resultado inmediato
                producer.flush()

    except KeyboardInterrupt:
        print("\nCerrando Consumer...")
        consumer.close()