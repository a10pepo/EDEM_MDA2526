# Post Work: Data Processing with Kafka end to end.

## Introduction
**In this exercise you will be implementing a real use case, creating data in real-time and making it available for reporting, by using Kafka.**


To do so, 1) create input data, 2) send it to a topic, 3) process it with a Consumer, 4) and then process it with KSQL , 5) and then show the
result on a termnial creen.

Feel free to exchange step 3) and 4).


## The proposed architecture will be the following:

Data source --> Producer sends data to --> Apache Kafka Topic --> Consumer reads data, filters it, process it, modify it and then sends
the processed data to another -> Apache Kafka Topic --> Process the data with KSQL and put it in another topic --> Consumer reads the data and
print the final messages on the terminal screen(Visual Estudio)

In any case, feel free to implement the use case using other alternatives, though at least 1) transforming data with a Consumer
and 2) transforming data with KSQL.

## Use case
These are typical use cases:

Transaction logging: Purchases, test scores, movies watched and movie latest location
Tracking pretty much anything including order status, packages, etc.
Storing health tracker data
Weather service history
Internet of things (IoT) status and event history
You will have to which use case to use, based on the previous list or a new one you choose.

## Tasks
You will have to perform the following tasks:

## Define your use case
Define/explain the Target of your application from a Business Point of view.
Find a dataset
Define/explain the data model (the json messages to be processed, the intermediate json messages while processing/transforming the data), and the final json message.

## Deliverables
You will have to provide the following:

Basic explanation of:
1. Use case
2.Dataset selected 
2. Final architecture implemented 
3. Json examples of your data json model 
4. **Evidence** of the Application has run end to end providing the expected results. With screenshots of the different step: 1)the ingestion, 2) the processing with a Consumer, 3) the processing with KSQL, the final printing on screen on the expected outcome.

**OJO** Si te fijas, Rubén, la ruta de las capturas es la de "PROFESORES/MDA/KAFKA..." Eso es fruto de un error que he cometido: Había hecho el ejercicio en otra carpeta y lo he tenido que mover aquí.


----
La práctica consiste en una arquitectura End-to-End de procesamiento de datos en streaming utilizando Apache Kafka, enfocada en un caso de uso Fintech para la normalización de pagos y detección de fraude.

El pipeline de datos consta de tres fases principales:

Ingesta: Un Producer en Python genera transacciones sintéticas con datos aleatorios (divisas variadas y estados de éxito/error).

Procesamiento (ETL): Un Consumer en Python actúa como intermediario, filtrando en tiempo real las operaciones fallidas y normalizando matemáticamente las divisas (USD/GBP) a una moneda estándar (EUR).

Analítica en Tiempo Real: Finalmente, utilizamos KSQL para monitorizar el flujo de datos limpio, aplicando una regla de negocio que detecta automáticamente transacciones de alto valor (> 3.000€) y emite alertas de riesgo ("HIGH_VALUE_ALERT") a un topic final de seguridad.
