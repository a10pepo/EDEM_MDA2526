# VALENBISI - Análisis de Uso de Bicicletas Públicas

## Descripción

Valencia cuenta con un sistema de bicicletas públicas llamado Valenbisi, gestionado por la ciudad. El objetivo de este ejercicio es crear un sistema completo de captura, procesamiento, visualización y replicación de datos sobre el uso de estas bicicletas utilizando la API de datos abiertos de la ciudad de Valencia.

Este ejercicio integrará múltiples tecnologías y conceptos aprendidos durante el curso para crear un pipeline de datos end-to-end que permita analizar el comportamiento del uso de bicicletas públicas en la ciudad.

## API de Datos Abiertos de Valencia

La ciudad de Valencia proporciona acceso a datos en tiempo real sobre el estado de las estaciones de Valenbisi a través de su API de datos abiertos:

**Endpoint:** `https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records?limit=20`

La API devuelve información sobre:
- Ubicación de las estaciones
- Número de bicicletas disponibles
- Número de espacios libres
- Estado de la estación (operativa/no operativa)
- Capacidad total de la estación

## Instrucciones

- Todo el código debe estar en Python.
- Todos los scripts deben estar en un docker compose para facilitar su despliegue y ejecución.

## Requisitos

El objetivo de este ejercicio es servir de proyecto integrador de los conocimientos adquiridos en el curso. Por tanto, se deben utilizar todos los conceptos aprendidos. En concreto, se deben completar las siguientes fases:

### 1. **Fase 1: Consumo de API y Almacenamiento**

Durante esta fase el objetivo es crear un script de Python que consuma la API de Valenbisi de forma periódica y almacene los datos en una base de datos SQL.

**Requisitos:**

- Crear un script `valenbisi_collector.py` que:
  - Consulte la API de Valenbisi cada 5 minutos
  - Extraiga la información relevante de cada estación:
    - ID de la estación
    - Nombre de la estación
    - Coordenadas (latitud, longitud)
    - Número de bicicletas disponibles
    - Número de espacios libres
    - Estado de la estación
    - Timestamp de la consulta
  - Almacene los datos en una tabla de PostgreSQL llamada `valenbisi_raw`

**Estructura de la tabla `valenbisi_raw`:**

```sql
CREATE TABLE valenbisi_raw (
    id SERIAL PRIMARY KEY,
    station_id INTEGER NOT NULL,
    station_name VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    available_bikes INTEGER,
    available_slots INTEGER,
    station_status VARCHAR(50),
    total_capacity INTEGER,
    timestamp TIMESTAMP NOT NULL
);
```

EXTRA: ¿Podrías crear un diagrama de Tablas y Relaciones (ERD) para este esquema de base de datos?

### 2. **Fase 2: Transformación con DBT**

Una vez que tenemos los datos almacenados en bruto, debemos transformarlos para facilitar su análisis. En esta fase utilizaremos DBT (Data Build Tool) para crear modelos agregados.

**Requisitos:**

- Instalar y configurar DBT para conectarse a la base de datos PostgreSQL
- Crear los modelos necesarios para una visión diaria y horaria del uso de bicicletas



### 3. **Fase 3: Visualización con Dashboard**

Con los datos ya procesados y agregados, es momento de crear visualizaciones que permitan analizar el uso de las bicicletas de forma intuitiva.

**Requisitos:**

Crear un dashboard que represente los datos por estación y por franjas horarias. 

### 4. **Fase 4: Almacenamiento Base de Datos NoSQL**

Modificar el script original para que también almacene los datos procesados en una base de datos NoSQL (MongoDB) para consultas rápidas y escalables.


