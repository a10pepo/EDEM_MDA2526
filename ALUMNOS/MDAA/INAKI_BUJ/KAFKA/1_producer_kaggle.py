from confluent_kafka import Producer
import json
import time
import csv
import random
from colorama import Fore, init

# Inicializar colores
init(autoreset=True)

# --- CONFIGURACIÓN ---
topic_name = 'raw_transactions'  # El topic donde enviaremos los datos
conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

# --- DATOS SIMULADOS (Para enriquecer la demo) ---
nombres = ['Alice', 'Bob', 'Carlos', 'Diana', 'Eduardo', 'Fernanda', 'Gustavo', 'Hilda']
paises = ['ES', 'US', 'FR', 'DE', 'MX', 'AR', 'CO']
tipos_tarjeta = ['Visa', 'MasterCard', 'Amex']

print(Fore.CYAN + "🚀 Iniciando Productor de Transacciones Financieras...")
print(Fore.CYAN + "📂 Leyendo 'creditcard.csv' y traduciendo columnas...")

try:
    with open('creditcard.csv', 'r') as file:
        reader = csv.DictReader(file)
        
        counter = 0
        for row in reader:
            # 1. FILTRADO: Para no saturar, procesamos solo algunas o si es fraude
            es_fraude_real = int(row['Class'])
            
            # Si NO es fraude y el dado dice que no (90% prob), saltamos para ir rápido
            if es_fraude_real == 0 and random.randint(1, 10) != 1:
                continue

            # 2. TRADUCCIÓN Y ENRIQUECIMIENTO (Aquí ponemos los "Títulos" bonitos)
            mensaje_bonito = {
                "id_transaccion": f"TXN-{100000 + counter}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                
                # Datos Legibles (Traducidos del CSV)
                "monto_original": float(row['Amount']),
                "es_fraude": True if es_fraude_real == 1 else False,
                
                # Datos Simulados (Para darle contexto de negocio)
                "cliente": random.choice(nombres),
                "pais_origen": random.choice(paises),
                "tarjeta": random.choice(tipos_tarjeta),
                
                # Mantenemos un dato técnico por si acaso (ej. V1)
                "factor_riesgo_v1": round(float(row['V1']), 4)
            }

            # 3. ENVIAR A KAFKA
            producer.produce(topic_name, json.dumps(mensaje_bonito).encode('utf-8'))
            
            # 4. FEEDBACK EN PANTALLA (Para que tú lo veas claro)
            color = Fore.RED if mensaje_bonito['es_fraude'] else Fore.GREEN
            icono = "🚨" if mensaje_bonito['es_fraude'] else "✅"
            
            print(color + f"{icono} Enviado: {mensaje_bonito['id_transaccion']} | "
                          f"Cliente: {mensaje_bonito['cliente']} ({mensaje_bonito['pais_origen']}) | "
                          f"Monto: {mensaje_bonito['monto_original']}")
            
            producer.flush()
            counter += 1
            
            # Pausa pequeña para dar efecto de "Tiempo Real"
            time.sleep(0.5)

except FileNotFoundError:
    print(Fore.RED + "❌ Error: No encuentro 'creditcard.csv'. Asegúrate de que está en la misma carpeta.")
except KeyboardInterrupt:
    print(Fore.YELLOW + "\n⏹️ Productor detenido por el usuario.")