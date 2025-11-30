from confluent_kafka import Producer
from colorama import Fore, Style, init
import json
import time
import csv
import os

# Inicializar colorama para colores en consola
init(autoreset=True)

CONF = {
    "bootstrap.servers": "localhost:9092"
}

TOPIC_RAW = "signos_vitales_raw"


def delivery_report(err, msg):
    """Callback que se ejecuta cuando Kafka confirma el envío."""
    if err is not None:
        print(Fore.RED + f"❌ Error al enviar mensaje: {err}")
    else:
        print(
            Fore.GREEN
            + f"✅ Enviado signos paciente {msg.key().decode('utf-8')} al topic {msg.topic()}"
        )


def leer_mediciones_desde_csv(ruta_csv):
    """Lee el CSV y devuelve una lista de diccionarios."""
    mediciones = []
    with open(ruta_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mediciones.append({
                "paciente_id": row["paciente_id"],
                "habitacion": row["habitacion"],
                "edad": int(row["edad"]),
                "diagnostico_base": row["diagnostico_base"],
                "frecuencia_cardiaca": float(row["frecuencia_cardiaca"]),
                "tension_sistolica": float(row["tension_sistolica"]),
                "tension_diastolica": float(row["tension_diastolica"]),
                "saturacion_oxigeno": float(row["saturacion_oxigeno"]),
                "temperatura": float(row["temperatura"]),
                "timestamp": row["timestamp"],
            })
    return mediciones


def main():
    producer = Producer(CONF)

    ruta_csv = os.path.join("signos_pacientes.csv")  # mismo directorio
    mediciones = leer_mediciones_desde_csv(ruta_csv)

    print(Fore.CYAN + Style.BRIGHT + "🏥 Iniciando productor de signos vitales (CSV → JSON → Kafka)...")

    try:
        for medicion in mediciones:
            key = medicion["paciente_id"]

            # Transformación CSV -> dict -> JSON
            producer.produce(
                TOPIC_RAW,
                key=key.encode("utf-8"),
                value=json.dumps(medicion).encode("utf-8"),
                callback=delivery_report,
            )

            # procesar callbacks
            producer.poll(0)
            time.sleep(0.2)  # para que se vea “en tiempo real”

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n🛑 Productor interrumpido por el usuario.")
    finally:
        print(Fore.CYAN + "⏳ Vaciando mensajes pendientes...")
        producer.flush()
        print(Fore.CYAN + "✅ Productor detenido correctamente.")


if __name__ == "__main__":
    main()