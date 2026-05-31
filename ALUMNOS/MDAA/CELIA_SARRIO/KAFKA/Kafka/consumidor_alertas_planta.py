from confluent_kafka import Consumer
import json
import time
from colorama import Fore, Style, init

init(autoreset=True)

CONF_CONSUMER = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "equipo_planta_v1",
    "auto.offset.reset": "earliest",
}

TOPIC_ALERTAS = "alertas_planta_topic"


def get_field(d, *names):
    for name in names:
        if name in d:
            return d[name]
    return None


def pintar_alerta_planta(datos):
    paciente_id = get_field(datos, "paciente_id", "PACIENTE_ID")
    habitacion = get_field(datos, "habitacion", "HABITACION")
    edad = get_field(datos, "edad", "EDAD")
    diag = get_field(datos, "diagnostico_base", "DIAGNOSTICO_BASE")
    estado = get_field(datos, "estado_clinico", "ESTADO_CLINICO")
    segmento = get_field(datos, "segmento_paciente", "SEGMENTO_PACIENTE")
    prioridad = get_field(datos, "prioridad_atencion", "PRIORIDAD_ATENCION")

    momento = time.strftime("%Y-%m-%d %H:%M:%S")

    print(
        Fore.YELLOW
        + Style.BRIGHT
        + f"⚠️ [PLANTA][{momento}] Revisión prioritaria | Paciente {paciente_id} (hab. {habitacion})\n"
          f"    Edad: {edad} | Diagnóstico: {diag} | Segmento: {segmento} | Estado: {estado} | Prioridad: {prioridad}\n"
    )


def main():
    consumer = Consumer(CONF_CONSUMER)
    consumer.subscribe([TOPIC_ALERTAS])

    print(
        Fore.CYAN
        + Style.BRIGHT
        + f"📡 [PLANTA] Escuchando alertas moderadas en topic {TOPIC_ALERTAS}"
    )

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(Fore.RED + f"❌ Error consumer Planta: {msg.error()}")
                continue

            datos = json.loads(msg.value().decode("utf-8"))
            pintar_alerta_planta(datos)

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n🛑 Consumer Planta interrumpido.")
    finally:
        consumer.close()
        print(Fore.CYAN + "✅ Consumer Planta detenido.")


if __name__ == "__main__":
    main()
