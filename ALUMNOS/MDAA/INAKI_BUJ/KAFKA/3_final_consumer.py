from confluent_kafka import Consumer
import json
import time
from colorama import Fore, Style, init

init(autoreset=True)

# --- CONFIGURACIÓN ---
conf = {
    'bootstrap.servers': 'localhost:9092', # Tu puerto configurado
    'group.id': 'grupo_policia_final',
    'auto.offset.reset': 'latest'
}

consumer = Consumer(conf)
# Nos suscribimos al topic que creó KSQL
consumer.subscribe(['alertas_finales'])

print(Fore.RED + Style.BRIGHT + "👮 MONITOR DE SEGURIDAD ACTIVADO")
print(Fore.RED + "   Esperando alertas de alto riesgo filtradas por KSQL...")

try:
    while True:
        msg = consumer.poll(1.0)
        
        if msg is None: continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue

        # Decodificar
        datos = json.loads(msg.value().decode('utf-8'))
        
        # En KSQL a veces los campos vienen en MAYÚSCULAS o minúsculas dependiendo de la versión
        # Hacemos un pequeño truco para leerlo seguro:
        cliente = datos.get('CLIENTE') or datos.get('cliente')
        pais = datos.get('PAIS') or datos.get('pais')
        riesgo = datos.get('RIESGO_CALCULADO') or datos.get('riesgo_calculado')
        monto = datos.get('MONTO_USD') or datos.get('monto_usd')

        # --- IMPRESIÓN FINAL EN PANTALLA ---
        print(Fore.RED + "----------------------------------------------------")
        print(Fore.RED + Style.BRIGHT + f"🚨 ALERTA DE FRAUDE DETECTADA (KSQL STREAM)")
        print(Fore.WHITE + f"   👤 Sospechoso: {cliente} ({pais})")
        print(Fore.WHITE + f"   💰 Monto: ${monto}")
        print(Fore.YELLOW + Style.BRIGHT + f"   ⚠️  NIVEL DE RIESGO: {riesgo}/100")
        print(Fore.RED + "----------------------------------------------------")

except KeyboardInterrupt:
    print("Monitor detenido.")
finally:
    consumer.close()