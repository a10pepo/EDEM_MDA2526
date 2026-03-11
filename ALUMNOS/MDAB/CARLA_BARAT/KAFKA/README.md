Proyecto Kafka: Monitorización de Cadena de Frío 

Introducción
En este proyecto he desarrollado un pipeline de datos en tiempo real para controlar la temperatura de productos sensibles (comida y medicamentos) durante su logística. El objetivo es que, si un sensor detecta que la temperatura sube de 5°C, el sistema genere una alerta automática.

Mi Arquitectura
He diseñado un flujo de datos que pasa por tres etapas principales:

Ingesta de Datos: He creado un script en Python (producer.py) que lee un archivo de texto con una serie de registros de sensores y los envía a un topic de Kafka llamado lecturas-temperatura.

Transformación y Enriquecimiento: He programado un segundo script (transformer.py) que hace de "puente". Lee los datos del primer topic, les añade información extra (como el ID del almacén de Valencia y la unidad de medida) y los vuelve a publicar en un topic nuevo.

Análisis de Alertas: He utilizado KSQL para crear un stream que filtra en tiempo real. Si la temperatura es superior a 5.0, el sistema genera una alerta con un mensaje de riesgo.

Componentes del Proyecto
docker-compose.yml: Para levantar todo el ecosistema (Broker, Zookeeper, KSQL, etc.).

producer.py: Mi script para simular el envío de datos de los sensores.

transformer.py: Mi lógica de procesamiento que enriquece el JSON original.

sensor_temperatura.txt: El dataset que he preparado con 40 casos de prueba realistas.

Cómo ejecutar mi proyecto
Para ponerlo en marcha, sigo estos pasos en diferentes terminales:

Levantar Docker:

Bash
docker-compose up -d
Ejecutar mi Transformer (Escucha):

Bash
python3 transformer.py
Ejecutar mi Producer (Envío):

Bash
python3 producer.py
Consultar Alertas en KSQL: Accedo al CLI de KSQL y lanzo la consulta:

SQL
SELECT * FROM alertas_cadena_frio EMIT CHANGES;