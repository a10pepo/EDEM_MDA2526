# 🚀 End-to-End Real-Time Data Pipeline con Apache Kafka

![Kafka](https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![KSQL](https://img.shields.io/badge/KSQL-Stream_Processing-blueviolet?style=for-the-badge)

## 📋 Resumen Ejecutivo

Este proyecto implementa una arquitectura de **Ingeniería de Datos en Streaming** diseñada para procesar transacciones bancarias en tiempo real. El sistema simula un entorno de producción donde la seguridad del dato (*Data Privacy*) y la analítica inmediata son críticas.

El pipeline ingesta datos crudos, aplica transformaciones ETL para anonimizar información sensible (cumplimiento PCI-DSS/GDPR) y agrega métricas de negocio utilizando **KSQLDB**.

---

## 1. Definición del Caso de Negocio
**Escenario: Monitorización de Ventas y Prevención de Fraude en E-Commerce**

En el sector financiero y retail, el análisis de transacciones no puede esperar al cierre del día (Batch). Sin embargo, los datos transaccionales contienen información personal altamente sensible (PII), como números de tarjetas de crédito, que no deben exponerse en capas analíticas.

**Objetivos del Proyecto:**
1.  **Ingesta en Tiempo Real:** Capturar transacciones al instante de producirse simulando un TPV.
2.  **Seguridad y Privacidad:** Eliminar datos sensibles (tarjetas de crédito) antes de su almacenamiento.
3.  **Inteligencia de Negocio:** Calcular el volumen de ventas e ingresos totales por categoría en vivo.

---

## 2. Arquitectura de la Solución

El flujo de datos ("Pipeline") se ha diseñado siguiendo el patrón **Producer-Processor-Consumer**:

```mermaid
graph LR
    A[📦 Source: Producer Python] -->|JSON Raw| B((Kafka Topic: raw-transactions))
    B --> C[⚙️ ETL Processor: Python Consumer]
    C -->|Lógica de Filtrado & Masking| D((Kafka Topic: clean-transactions))
    D --> E[📊 Analytics: KSQLDB Engine]
    E -->|Agregación SQL| F[📈 Tabla: VENTAS_STATS]
Ingesta: Script en Python que genera datos sintéticos aleatorios.

ETL (Extract, Transform, Load): El procesador actúa como Middleware, interceptando el mensaje para eliminar el campo tarjeta_credito y normalizar la categoria a mayúsculas.

Analytics: KSQL realiza sumas y conteos sobre el stream de datos limpios.

3. Modelo de Datos (Data Governance)
A continuación se detalla la evolución del esquema del mensaje JSON a través del pipeline:

A. Datos de Entrada (Raw Layer)
Origen: Producer | Tópico: raw-transactions

Nota: Contiene datos sensibles expuestos.

JSON
{
  "id_transaccion": 5291,
  "cliente": "Carlos",
  "tarjeta_credito": "4500-1234-5678-9010", 
  "categoria": "hogar",
  "monto": 120.50
}
B. Datos Procesados (Clean Layer)
Origen: Processor | Tópico: clean-transactions

Nota: Se ha aplicado anonimización y enriquecimiento de metadatos.

JSON
{
  "id_transaccion": 5291,
  "cliente": "Carlos",
  "categoria": "HOGAR", 
  "monto": 120.50,
  "procesado_por": "ETL_Python_v1"
}
C. Métricas de Negocio (Gold Layer)
Origen: KSQL | Tabla: VENTAS_STATS

Nota: Agregación en tiempo real con formato monetario.

JSON
{
  "CATEGORIA": "HOGAR",
  "TOTAL_PEDIDOS": 58,
  "TOTAL_INGRESOS": 16874.52
}
4. Stack Tecnológico y Configuración
El proyecto se despliega sobre contenedores Docker para garantizar la portabilidad.

Zookeeper & Kafka Broker: Confluent Community Edition (v7.4.0).

KSQLDB Server & CLI: Motor de SQL para stream processing.

Python 3.x: Librería kafka-python para la lógica de aplicación.

Configuración del Entorno: Se ha optimizado el clúster para ejecutarse en un entorno de desarrollo (Single Node) ajustando las réplicas y el ISR en el docker-compose.yml:

YAML
KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
5. Lógica de Negocio (KSQL)
La transformación final se realiza mediante una consulta declarativa SQL que persiste el estado de las ventas:

SQL
CREATE TABLE ventas_stats AS
SELECT 
    categoria, 
    COUNT(*) AS total_pedidos, 
    -- Casteo a decimal para precisión monetaria (2 decimales)
    CAST(SUM(monto) AS DECIMAL(10,2)) AS total_ingresos
FROM clean_stream
GROUP BY categoria
EMIT CHANGES;
6. Evidencias de Ejecución (End-to-End)
Fase 1: Ingesta de Datos
El Productor envía transacciones simuladas al clúster cada 2 segundos.

Fase 2: Procesamiento ETL
El Consumidor intercepta, limpia (elimina tarjeta) y reenvía los datos transformados.

Fase 3: Visualización Final
Dashboard en tiempo real mostrando los ingresos acumulados por categoría correctamente formateados.

Autor: Rafa Morata | Máster de Data Engineering