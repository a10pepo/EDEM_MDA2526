from confluent_kafka import Consumer, Producer
import json
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Configuración del consumidor que lee del topic de entrada
CONF_CONSUMER = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "grupo_enriquecedor_signos",
    "auto.offset.reset": "earliest",
}

# Configuración del productor que escribe al topic enriquecido
CONF_PRODUCER = {
    "bootstrap.servers": "localhost:9092",
}

TOPIC_ORIGEN = "signos_vitales_raw"
TOPIC_DESTINO = "signos_vitales_enriquecidos"


def calcular_segmento_paciente(edad, diagnostico_base):
    """
    Segmentamos al paciente según edad y diagnóstico base.
    - ALTO_RIESGO: edad >= 70 o cardiopatía / EPOC
    - NORMAL: resto
    """
    diagnostico = (diagnostico_base or "").lower()
    if edad >= 70 or diagnostico in ("cardiopatia", "epoc"):
        return "ALTO_RIESGO"
    return "NORMAL"


def calcular_estado_clinico(fc, tas, tad, spo2, temp):
    """
    Clasificamos al paciente según sus signos vitales:
    - CRITICO: valores claramente fuera de rango
    - ALERTA: valores intermedios
    - ESTABLE: todo ok
    """
    # Estado CRÍTICO
    if spo2 < 90 or fc > 130 or tas >= 180 or temp >= 39.0:
        return "CRITICO"

    # Estado de ALERTA
    if (
        90 <= spo2 < 94
        or 140 <= tas < 180
        or 110 <= fc <= 130
        or 38.0 <= temp < 39.0
    ):
        return "ALERTA"

    # Estado ESTABLE
    return "ESTABLE"


def calcular_prioridad_atencion(estado_clinico, segmento_paciente):
    """
    Asignamos prioridad al paciente:
    - MUY_ALTA: estado CRITICO
    - ALTA: estado ALERTA o ESTABLE + ALTO_RIESGO
    - NORMAL: resto
    """
    if estado_clinico == "CRITICO":
        return "MUY_ALTA"
    if estado_clinico == "ALERTA":
        return "ALTA"
    if estado_clinico == "ESTABLE" and segmento_paciente == "ALTO_RIESGO":
        return "ALTA"
    return "NORMAL"


def main():
    consumer = Consumer(CONF_CONSUMER)
    producer = Producer(CONF_PRODUCER)

    consumer.subscribe([TOPIC_ORIGEN])

    print(
        Fore.CYAN
        + Style.BRIGHT
        + f"🔄 Iniciando consumidor enriquecedor (lee {TOPIC_ORIGEN} → escribe {TOPIC_DESTINO})"
    )

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                # No hay mensajes nuevos en este momento
                continue

            if msg.error():
                print(Fore.RED + f"❌ Error en el consumer: {msg.error()}")
                continue

            # Mensaje correcto → parseamos el JSON
            datos = json.loads(msg.value().decode("utf-8"))

            paciente_id = datos.get("paciente_id")
            edad = float(datos.get("edad", 0))
            diagnostico_base = datos.get("diagnostico_base", "")

            fc = float(datos.get("frecuencia_cardiaca", 0))
            tas = float(datos.get("tension_sistolica", 0))
            tad = float(datos.get("tension_diastolica", 0))
            spo2 = float(datos.get("saturacion_oxigeno", 0))
            temp = float(datos.get("temperatura", 0))

            segmento = calcular_segmento_paciente(edad, diagnostico_base)
            estado = calcular_estado_clinico(fc, tas, tad, spo2, temp)
            prioridad = calcular_prioridad_atencion(estado, segmento)

            enriched = {
                **datos,
                "segmento_paciente": segmento,
                "estado_clinico": estado,
                "prioridad_atencion": prioridad,
            }

            # Enviamos el mensaje enriquecido al nuevo topic
            producer.produce(
                TOPIC_DESTINO,
                key=paciente_id.encode("utf-8"),
                value=json.dumps(enriched).encode("utf-8"),
            )
            producer.poll(0)

            print(
                Fore.GREEN
                + f"✨ Paciente {paciente_id} (hab. {datos.get('habitacion')}) "
                  f"→ segmento={segmento}, estado={estado}, prioridad={prioridad}"
            )

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n🛑 Enriquecedor interrumpido por el usuario.")
    finally:
        consumer.close()
        producer.flush()
        print(Fore.CYAN + "✅ Enriquecedor detenido correctamente.")


if __name__ == "__main__":
    main()
