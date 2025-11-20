🚀 Proyecto: Laboratorio de PySpark Streaming con Docker 🐳
Este repositorio contiene un entorno de desarrollo encapsulado en Docker para simular y procesar un flujo de datos en tiempo real (similar a Kafka) utilizando PySpark Structured Streaming.

El objetivo de este laboratorio es que el alumno comprenda el flujo completo: Generación de Datos (Productor) → Cola de Mensajes (Directorio) → Consumo y Transformación (PySpark) → Almacenamiento Estático (Data Lake).

🎯 Objetivo de la Práctica
Aprender a:

Orquestar entornos de desarrollo con Docker Compose (levantar Jupyter y PySpark).

Configurar PySpark Structured Streaming para leer datos que llegan continuamente.

Implementar transformaciones ETL (Extract, Transform, Load) en un stream de datos.

Persistir un stream de datos en un formato eficiente (Parquet) para análisis posterior (Data Lake).

💡 El Flujo de Trabajo Simulado (Diagrama Conceptual)
En un entorno real, usaríamos Kafka. En este laboratorio, usamos el sistema de archivos local para simular la cola de mensajes.

Etapa	Componente	Acción	Simulación de...
Productor	Script Python (Celda 1)	Escribe lotes de archivos .json cada 1.5 segundos.	Envío de mensajes a un Tópico de Kafka.
Cola / Tópico	Carpeta /streaming_data	El directorio donde residen los archivos JSON.	El Broker de Kafka (almacenamiento de logs).
Consumidor	PySpark (Celda 2)	Monitoriza continuamente la carpeta (readStream) y procesa cada nuevo archivo como un nuevo lote.	Suscripción a un Tópico de Kafka.
Sink	PySpark (Celda 2)	Guarda los datos transformados en archivos Parquet en el disco.	Guardado en un Data Lake o Base de Datos.
🛠️ Requisitos e Inicialización
Solo necesitas tener Docker y Docker Compose instalados en tu máquina.

1. Levantar el Entorno (Docker)
En la raíz del proyecto (donde se encuentra docker-compose.yml), ejecuta:

Bash

docker compose up -d
Esto descargará la imagen de Jupyter/PySpark y levantará el contenedor en segundo plano.

2. Acceder al Jupyter Notebook
Abre tu navegador y accede a la URL:

http://localhost:8888
Cuando te pida la contraseña o token, usa: clase_spark

3. Ejecutar el Notebook
Abre el notebook que contiene el código de 3 celdas (o el que tú nos proporcionaste).

Ejecuta la Celda 1 para configurar la sesión de Spark y lanzar el Productor en segundo plano.

Ejecuta la Celda 2 para iniciar el Consumidor Streaming que leerá los datos y los guardará en Parquet.

Espera unos segundos para que se generen y procesen varios lotes.

📚 Código Explicado Detalladamente
El notebook está dividido en tres etapas clave:

A. Celda 1: Producción y Setup
Lógica: Lanza una función de Python en un hilo separado (hilo Productor). Este productor escribe archivos .json cada 1.5 segundos en la carpeta ./streaming_data.

Archivos Clave: Crea dos directorios:

./streaming_data (Nuestra cola de mensajes de entrada).

./checkpoint (Donde PySpark guarda su estado para saber qué ha leído y evitar re-procesar datos, crucial en streaming).

B. Celda 2: Consumo y Persistencia (Tu Tarea Principal)
Aquí es donde PySpark entra en acción.

Lectura Streaming: Se define el streaming_df usando spark.readStream.json(OUTPUT_DIR). PySpark comienza a monitorizar el directorio.

Transformación: El código de ejemplo filtra todas las alertas que no son "LOW" y añade una marca de tiempo de procesamiento (processed_at).

Doble Sink (Destino):

Sink 1 (Console): Imprime los datos transformados en la salida del notebook cada 5 segundos. Permite la visualización en tiempo real.

Sink 2 (Parquet): Usa .format("parquet") para guardar los datos transformados de forma incremental en el directorio ./final_processed_data. Esta es la creación de tu DataFrame Físico (Data Lake).

C. Celda 3: Análisis Estático (La Conclusión)
Detención: Se usa un bucle para detener todas las consultas de streaming activas, liberando los recursos de Spark.

Carga Estática: Se utiliza la lectura estándar de Spark (spark.read.parquet(FINAL_PARQUET_DIR)) para cargar el DataFrame Físico completo, consolidando todos los archivos Parquet guardados por el stream.

Análisis: Se ejecuta una consulta de ejemplo (groupBy, count) sobre el DataFrame estático para demostrar que el análisis histórico ahora es posible.

🛑 Detener y Limpiar el Entorno
Cuando termines la práctica, detén y elimina el contenedor para liberar recursos del sistema:

Detener la Ejecución del Notebook: Asegúrate de ejecutar la Celda 3 para detener las consultas de streaming internas.

Detener el Contenedor Docker: En tu terminal:

Bash

docker compose down
