# Proyecto Kafka End-to-End: Sistema de Tracking de Pedidos

##  Use Case

**Sistema de Tracking de Pedidos de E-commerce**

Monitoreo en tiempo real del estado de pedidos de una tienda online, detectando pedidos de alto valor y generando estadísticas agregadas por estado.

---

##  Objetivo del Negocio

- Procesar pedidos en tiempo real
- Clasificar pedidos por prioridad (HIGH, MEDIUM, LOW) según su precio
- Categorizar productos (Electronics, Home Appliances, Gaming)
- Generar estadísticas agregadas por estado del pedido
- Visualizar resultados en tiempo real

---

##  Arquitectura

```
Producer (producer.py)
    ↓
Topic: raw-orders
    ↓
Consumer Processor (consumer_processor.py) → Filtra y enriquece datos
    ↓
Topic: processed-orders
    ↓
Consumer Aggregator (consumer_aggregator.py) → Calcula estadísticas
    ↓
Topic: orders-stats
    ↓
Consumer Final (consumer_final.py) → Visualización
```

---

##  Modelo de Datos

### Mensaje Original (raw-orders)
```json
{
  "order_id": "ORD-1001",
  "customer": "Juan Perez",
  "product": "Laptop Dell",
  "quantity": 1,
  "price": 899.99,
  "status": "PENDING",
  "timestamp": "2026-02-11T10:30:00"
}
```

### Mensaje Procesado (processed-orders)
```json
{
  "order_id": "ORD-1001",
  "customer": "Juan Perez",
  "product": "Laptop Dell",
  "quantity": 1,
  "price": 899.99,
  "status": "PENDING",
  "timestamp": "2026-02-11T10:30:00",
  "priority": "HIGH",
  "category": "Electronics"
}
```

### Mensaje Agregado (orders-stats)
```json
{
  "STATUS": "PENDING",
  "TOTAL_ORDERS": 15,
  "TOTAL_REVENUE": 12500.50,
  "AVG_ORDER_VALUE": 833.37
}
```


##  Instalación y Ejecución

### 1. Levantar Kafka con Docker Compose

```bash
docker-compose up -d
```

### 2. Crear Topics

```bash
docker exec kafka-kafka-1 kafka-topics --create --topic raw-orders --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
docker exec kafka-kafka-1 kafka-topics --create --topic processed-orders --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
docker exec kafka-kafka-1 kafka-topics --create --topic orders-stats --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 3. Instalar Dependencias Python

```bash
pip install kafka-python
```

### 4. Ejecutar Aplicación (4 terminales)

**Terminal 1 - Producer:**
```bash
python producer.py
```

**Terminal 2 - Consumer Processor:**
```bash
python consumer_processor.py
```

**Terminal 3 - Consumer Aggregator:**
```bash
python consumer_aggregator.py
```

**Terminal 4 - Consumer Final:**
```bash
python consumer_final.py
```

---

##  Estructura del Proyecto

```
kafka-project/
├── docker-compose.yml
├── producer.py
├── consumer_processor.py
├── consumer_aggregator.py
└── consumer_final.py
```

---

##  Componentes

### Producer
- Genera pedidos aleatorios cada 2 segundos
- Envía datos al topic `raw-orders`

### Consumer Processor
- Lee de `raw-orders`
- Agrega campos `priority` y `category`
- Envía a `processed-orders`

### Consumer Aggregator
- Lee de `processed-orders`
- Calcula estadísticas por estado
- Envía a `orders-stats`

### Consumer Final
- Lee de `orders-stats`
- Muestra resultados formateados en consola

---

##  Tecnologías Utilizadas

- **Apache Kafka** 7.5.0
- **Zookeeper** 7.5.0
- **Python** 3.x
- **kafka-python**
- **Docker & Docker Compose**

---

##  Resultados

El sistema procesa pedidos en tiempo real mostrando:

1. **Ingesta de datos** - Producer generando pedidos
2. **Procesamiento** - Consumer agregando prioridad y categoría
3. **Agregación** - Cálculo de estadísticas por estado
4. **Visualización** - Estadísticas finales en consola


Pablo Sánchez - EDEM MDA 2526