# Ejercicio Evaluable: PySpark + Kafka

## Objetivo

Demuestra tu dominio de PySpark y Kafka resolviendo un caso real de análisis de datos de operaciones de e-commerce en streaming.

---

## 1. Requisitos previos

- Tener Docker y Docker Compose instalados.
- Tener Python 3.8+ y pip.
- Instalar las siguientes librerías:
  - `confluent-kafka`
  - `pyspark`

```bash
pip install confluent-kafka pyspark
```

- Tener un entorno Kafka funcionando (puedes usar el siguiente docker-compose):

```yaml
version: '2'
services:
  zookeeper:
    image: wurstmeister/zookeeper:3.4.6
    ports:
      - "2181:2181"
  kafka:
    image: wurstmeister/kafka:2.12-2.2.1
    ports:
      - "9092:9092"
    environment:
      KAFKA_ADVERTISED_HOST_NAME: localhost
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

Lanza con:
```bash
docker-compose up -d
```

---

## 2. Generador de datos

Ejecuta el script `generador_kafka.py` para poblar el tópico `operaciones_ecommerce` con datos simulados:

```bash
python generador_kafka.py
```

---

## 3. Ejercicios evaluables (entrega obligatoria)

Crea un script PySpark llamado `pyspark-entregable.py` que consuma en streaming los datos del tópico `operaciones_ecommerce` de Kafka y resuelva los siguientes ejercicios, demostrando el uso de todo lo aprendido en clase:

1. **Carga y exploración**: Lee los datos del tópico y muestra el esquema y las primeras filas del DataFrame.
2. **Filtrado**: Muestra solo las operaciones con estado `Completada` y aquellas cuyo importe total sea mayor de 500€.
3. **Transformaciones**: Crea una columna nueva que clasifique las operaciones en 'ALTO' o 'BAJO' valor según si el total supera 700€.
4. **Agregaciones**: Calcula el total de ventas y el ticket medio por producto y por usuario.
5. **Joins**: Crea un DataFrame auxiliar con una lista de usuarios VIP y haz un join para mostrar solo sus operaciones.
6. **Funciones de ventana**: Para cada usuario, muestra la operación de mayor importe y la de menor importe usando funciones de ventana.
7. **UDFs**: Define una UDF que clasifique el método de pago como 'Digital' (PayPal, Criptomoneda) o 'Tradicional' (Tarjeta, Transferencia) y aplícala.
8. **Particionado**: Reparte el DataFrame en 4 particiones y muestra cuántos registros hay en cada partición.
9. **SQL y vistas temporales**: Registra el DataFrame como vista temporal y haz una consulta SQL para obtener el número de operaciones por cada estado y método de pago.
10. **Análisis libre**: Realiza un análisis adicional a tu elección (puede ser una visualización, ranking, correlación, etc.) y explica brevemente tu razonamiento.

**Requisitos:**
- El código debe estar bien estructurado y comentado.
- Debes mostrar resultados relevantes por consola.
- Se valorará la creatividad, la calidad del análisis y la variedad de técnicas empleadas.

---

## 4. Entrega

- El alumno debe entregar el script `pyspark-entregable.py` con todo el código y los resultados impresos por consola.
- El código debe estar bien comentado y estructurado.

---

¡Suerte!