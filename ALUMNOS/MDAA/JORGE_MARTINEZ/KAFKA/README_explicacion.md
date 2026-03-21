# Monitorización de Tráfico en Tiempo Real con Apache Kafka y KSQL

Este proyecto implementa una arquitectura de procesamiento de datos en streaming para un caso de uso de **IoT (Internet de las Cosas)** enfocado en la seguridad vial.

## 1. Definición del Caso de Uso

### Objetivo Empresarial
El objetivo principal es mejorar la seguridad en las autopistas mediante la detección temprana de infracciones de velocidad. Desde una perspectiva de negocio, esta aplicación permite a las autoridades de tráfico:
1.  **Detectar en tiempo real** vehículos que superan el límite de velocidad permitido.
2.  **Clasificar la gravedad** de la infracción automáticamente.
3.  **Obtener métricas agregadas** por tramos (sensores) para identificar "puntos negros" donde se cometen más infracciones por minuto.

### Conjunto de Datos (Dataset)
Dado que es un sistema de tiempo real, se utilizan **datos sintéticos generados dinámicamente**.
Se simula una red de sensores de velocidad (`S-101`, `S-102`, etc.) ubicados en diferentes puntos de la carretera que envían telemetría cada segundo.

---

## 2. Arquitectura Implementada

El flujo de datos diseñado es el siguiente:

1.  **Origen:** Un script en Python (`producer.py`) simula sensores IoT.
2.  **Ingesta:** Los datos crudos entran al topic `traffic_raw`.
3.  **Procesamiento (Python):** Un consumidor (`processor.py`) lee los datos, filtra los vehículos que van a menos de 120 km/h (conductores legales) y enriquece los datos de los infractores añadiendo un nivel de gravedad.
4.  **Almacenamiento Intermedio:** Los datos procesados van al topic `traffic_speeding`.
5.  **Analítica (KSQL):** KSQL lee el flujo de infracciones y realiza una agregación por ventana de tiempo (Tumbling Window) de 1 minuto.
6.  **Resultado Final:** Se visualiza una tabla viva con el conteo de multas por sensor.

---

## 3. Modelo de Datos (JSON)

### A. Mensaje de Entrada (Raw Data)
Lo que envían los sensores al topic `traffic_raw`:
```json
{
  "sensor_id": "S-101",
  "vehicle_plate": "ABC-1234",
  "speed": 135,
  "lane": 2,
  "timestamp": 1678900000.123
}