# Caso de uso: Monitoreo en tiempo real de diferencias en expedición de un WMS
En una determinada empresa del sector de la alimentación, las entregas de expedición generadas por el gestor de almacén (SGA/WMS)pueden tener diferencias, entre lo que pidió el cliente y lo que realmente se expide. A este concepto se le denomina nivel de servicio y supone un KPI crítico para medir la fiabilidad del suministro. 

Como consecuencia de la creciente exigencia por parte de los clientes de mayores niveles de servicio y la falta de información cuando se dan faltas (en ocasiones no saben que no van a recibir el 100% hasta que abren el camión en la descarga), se requiere de un sistema que de forma eficiente genere alertas y permita automatizar el aviso a los clientes en estos momentos. 

# Diseño de la Arquitectura
El ecosistema está compuesto por cinco capas desacopladas que garantizan escalabilidad y tolerancia a fallos, todo orquestado mediante Docker:

Capa de Ingesta (Producer): Un servicio en Python que simula la salida de datos del WMS, enviando eventos brutos (Order ID, Cantidad Pedida, Cantidad Servida) al tópico entregas.

Capa de Mensajería (Kafka Broker): Actúa como el sistema nervioso central, almacenando y distribuyendo los eventos de forma persistente y ordenada.

Capa de Procesamiento (Stream Processor): Un consumidor Python que actúa como motor de reglas. Realiza el Data Enrichment calculando el porcentaje de rotura en tiempo real y clasificando la criticidad del incidente (OK, LEVE, GRAVE, MUY GRAVE). Los resultados enriquecidos se reenvían al tópico alertas_entregas.

Capa de Análisis (ksqlDB): Un motor de SQL por streaming que permite realizar consultas analíticas sobre los datos en movimiento sin necesidad de una base de datos relacional externa.

Capa de Orquestación (Zookeeper): Gestiona el estado y la configuración del cluster de Kafka.
