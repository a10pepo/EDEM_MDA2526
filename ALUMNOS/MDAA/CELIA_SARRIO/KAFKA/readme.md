# Sistema de Alertas Hospitalarias en Tiempo Real con Kafka y ksqlDB

## 1. Descripción general

Este proyecto implementa un sistema de **monitorización en tiempo real de pacientes hospitalizados** utilizando:

- **Apache Kafka** como sistema de mensajería.
- **ksqlDB** para el procesamiento de streams.
- Varias aplicaciones en **Python** como productores y consumidores.

Cada evento representa una medición de signos vitales de un paciente (frecuencia cardíaca, tensión arterial, saturación de oxígeno, temperatura, etc.).  
A partir de estos datos se:

1. **Enriquecen** los eventos con lógica de negocio (segmentación y estado clínico).
2. **Generan alertas** cuando el paciente está en riesgo.
3. **Enrutan las alertas** automáticamente a diferentes equipos asistenciales del hospital:
   - UCI
   - Planta
   - Seguimiento de pacientes de alto riesgo

El objetivo es simular un entorno realista donde diferentes equipos consumen, en paralelo, solo la información relevante para su trabajo.

---

## 2. Objetivos de la práctica

- Consumir datos desde un dataset en formato **CSV** y transformarlos a **JSON** antes de enviarlos a Kafka.
- Implementar un **productor** y varios **consumidores** en Python usando `confluent-kafka`.
- Utilizar **ksqlDB** para:
  - Definir streams sobre topics de Kafka.
  - Aplicar lógica de negocio (filtros y enrutado de eventos).
- Diseñar una arquitectura basada en **múltiples topics y grupos de consumidores**, simulando diferentes equipos dentro de un hospital.

---

## 3. Requisitos previos

### Software

- Docker y Docker Compose
- Python 3.x
- Entorno Kafka/KSQL proporcionado por el profesor (con `docker-compose.yml`)

### Dependencias Python

En la carpeta del proyecto:

```bash
pip install -r requirements.txt
