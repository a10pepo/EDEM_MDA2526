from confluent_kafka import Consumer
import json
import time
from colorama import Fore, Style, init

# Inicializar colorama para colores en consola
init(autoreset=True)

CONF_CONSUMER = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "grupo_alertas_pacientes",
    "auto.offset.reset": "earliest",
}

TOPIC_ALERTAS = "alertas_pacientes_topic"


def normalizar_claves(datos_raw: dict) -> dict:
    """
    ksqlDB suele sacar las claves en MAYÚSCULAS (PACIENTE_ID, HABITACION, etc.).
    Esta función pasa todas las claves a minúsculas para que podamos usar
    datos["paciente_id"], datos["habitacion"], etc.
    """
    return {str(k).lower(): v for k, v in datos_raw.items()}


def pintar_alerta(datos):
    paciente_id = datos.get("paciente_id")
    habitacion = datos.get("habitacion")
    edad = datos.get("edad")
    diagnostico_base = datos.get("diagnostico_base")
    estado = datos.get("estado_clinico")
    segmento = datos.get("segmento_paciente")
    prioridad = datos.get("prioridad_atencion")

    fc = datos.get("frecuencia_cardiaca")
    tas = datos.get("tension_sistolica")
    tad = datos.get("tension_diastolica")
    spo2 = datos.get("saturacion_oxigeno")
    temp = datos.get("temperatura")

    momento = time.strftime("%Y-%m-%d %H:%M:%S")

    # Elegimos icono y color según el estado
    if estado == "CRITICO":
        icono = "🚨"
        color = Fore.RED
    elif estado == "ALERTA":
        icono = "⚠️"
        color = Fore.YELLOW
    else:
        icono = "ℹ️"
        color = Fore.CYAN

    print(
        color
        + Style.BRIGHT
        + f"{icono} [{momento}] ALERTA PACIENTE {paciente_id} | Habitación {habitacion} | Edad: {edad} | "
          f"Diag: {diagnostico_base} | Estado: {estado} | Segmento: {segmento} | Prioridad: {prioridad} | "
          f"FC={fc} bpm, TA={tas}/{tad} mmHg, SatO2={spo2} %, Temp={temp} ºC"
    )


def main():
    consumer = Consumer(CONF_CONSUMER)
    consumer.subscribe([TOPIC_ALERTAS])

    print(
        Fore.CYAN
        + Style.BRIGHT
        + f"📡 Iniciando consumidor final de alertas (topic {TOPIC_ALERTAS})"
    )

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print(Fore.RED + f"❌ Error en el consumer de alertas: {msg.error()}")
                continue

            datos_raw = json.loads(msg.value().decode("utf-8"))

            # Normalizamos claves a minúsculas
            datos = normalizar_claves(datos_raw)

            # (Opcional) si quieres ver cómo viene realmente:
            # print("DEBUG JSON:", datos_raw)

            pintar_alerta(datos)

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n🛑 Consumer de alertas interrumpido por el usuario.")
    finally:
        consumer.close()
        print(Fore.CYAN + "✅ Consumer de alertas detenido.")


if __name__ == "__main__":
    main()

