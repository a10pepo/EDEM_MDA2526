
# 🚀 Laboratorio de PySpark Streaming con Docker 🐳

> Entorno de desarrollo encapsulado en Docker para simular y procesar un flujo de datos en tiempo real (tipo Kafka) usando **PySpark Structured Streaming**.

---

## 🎯 Objetivo de la Práctica

Comprender el flujo completo:

1. **Generación de Datos (Productor)**
2. **Cola de Mensajes (Directorio)**
3. **Consumo y Transformación (PySpark)**
4. **Almacenamiento Estático (Data Lake)**

### Aprenderás a:
- Orquestar entornos con **Docker Compose** (Jupyter + PySpark)
- Configurar **PySpark Structured Streaming** para leer datos en tiempo real
- Implementar transformaciones **ETL** en un stream de datos
- Persistir datos en formato **Parquet** para análisis posterior

---

## 💡 Flujo de Trabajo Simulado

En vez de Kafka, usamos el sistema de archivos local para simular la cola de mensajes.

| Etapa      | Componente                | Acción                                                        | Simulación de...                  |
|------------|--------------------------|---------------------------------------------------------------|-----------------------------------|
| Productor  | Script Python (Celda 1)  | Escribe lotes de archivos `.json` cada 1.5 segundos           | Envío de mensajes a un tópico     |
| Cola       | Carpeta `/streaming_data`| Directorio donde residen los archivos JSON                    | Broker de Kafka (logs)            |
| Consumidor | PySpark (Celda 2)        | Monitoriza la carpeta y procesa cada nuevo archivo            | Suscripción a un tópico           |
| Sink       | PySpark (Celda 2)        | Guarda los datos transformados en archivos Parquet            | Data Lake o Base de Datos         |

---

## 🛠️ Requisitos e Inicialización

- Tener **Docker** y **Docker Compose** instalados.

### 1. Levantar el entorno
En la raíz del proyecto (donde está `docker-compose.yml`):

```bash
docker compose up -d
```

Esto descargará la imagen y levantará el contenedor en segundo plano.

### 2. Acceder a Jupyter Notebook

Abre tu navegador y entra en:

[http://localhost:8888](http://localhost:8888)

Cuando pida contraseña/token, usa: `clase_spark`

### 3. Ejecutar el Notebook

- Abre el notebook de 3 celdas (o el que te proporcionamos)
- **Celda 1:** Configura Spark y lanza el Productor en segundo plano
- **Celda 2:** Inicia el Consumidor Streaming (lee y guarda en Parquet)
- Espera unos segundos para que se generen y procesen varios lotes

---

## 📚 Estructura del Código

### A. Celda 1: Producción y Setup
- Lanza una función Python en un hilo separado (Productor)
- Escribe archivos `.json` cada 1.5s en `./streaming_data`
- Crea dos carpetas:
	- `./streaming_data` (cola de entrada)
	- `./checkpoint` (estado de PySpark para evitar reprocesos)

### B. Celda 2: Consumo y Persistencia (**Tu tarea principal**)
- **Lectura Streaming:**
	- `spark.readStream.json(OUTPUT_DIR)` monitoriza el directorio
- **Transformación:**
	- Filtra alertas distintas de "LOW" y añade timestamp `processed_at`
- **Doble Sink:**
	- **Console:** imprime datos cada 5s en el notebook
	- **Parquet:** guarda datos en `./final_processed_data` (Data Lake)

### C. Celda 3: Análisis Estático (Conclusión)
- Detiene todas las consultas de streaming activas
- Carga el DataFrame físico completo con `spark.read.parquet(FINAL_PARQUET_DIR)`
- Ejemplo de análisis: `groupBy`, `count` sobre el DataFrame

---

## 🛑 Detener y Limpiar el Entorno

1. **Detener ejecución del notebook:** Ejecuta la Celda 3 para parar el streaming
2. **Detener el contenedor Docker:**

```bash
docke compose down
```

---

¡Listo! 🚦
