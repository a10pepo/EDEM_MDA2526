# Ejercicio 5: KSQL

## Objetivos
2. Usar KSQL para consultar los mensajes producidos desde una aplicación Kafka Python.

---

## Ejecutar Kafka en tu ordenador con Docker
Escenario simple:
- 1 Zookeeper
- 1 Broker Kafka
- 1 Servidor KSQL
- 1 CLI de KSQL

Inicia los contenedores de ZooKeeper y Kafka:

---

## Crear un nuevo topic en Kafka desde la línea de comandos
Ejecuta el productor desde la línea de comandos:
```sh
docker-compose exec kafka kafka-topics --create --topic palabras --partitions 1 --replication-factor 1 --if-not-exists --bootstrap-server localhost:9092
```

---

## Ejecutar la aplicación Productor en Python desde Visual Studio
Ejecuta el archivo `ejercicio_8_ksql/producer.py`. Este productor enviará frases del libro *El Quijote*.

Comprueba que los mensajes (cada palabra del libro) se están enviando al topic `palabras`:
```sh
docker-compose exec kafka kafka-console-consumer --topic palabras --from-beginning --bootstrap-server localhost:9092
```

Si ves los mensajes llegando, ¡todo está correcto! Sal con **Control-C**.

---

## Abrir KSQL en una consola
```sh
docker-compose exec ksql-cli ksql http://host.docker.internal:8088
```

Deberías ver algo como esto:
```
⏳ Waiting for KSQL to be available before launching CLI

      ===========================================
      =        _  __ _____  ____  _             =
      =       | |/ // ____|/ __ \| |            =
      =       | ' /| (___ | |  | | |            =
      =       |  <  \___ \| |  | | |            =
      =       | . \ ____) | |__| | |____        =
      =       |_|\_\_____/ \___\_\______|       =
      =                                         =
      =  Streaming SQL Engine for Apache Kafka® =
      ===========================================
Copyright 2017-2019 Confluent Inc.

CLI v5.4.1, Server v<unknown> located at http://ksql-server:8088
```

---

## Consultar los mensajes del topic con KSQL
Primero, ajusta el offset para leer desde el principio:
```sql
SET 'auto.offset.reset' = 'earliest';
```

Ver los topics:
```sql
SHOW TOPICS;
```

Resultado esperado:
```
Kafka Topic  | Partitions | Partition Replicas
------------------------------------------------
 palabras     | 1          | 1
------------------------------------------------
```

Imprimir los mensajes:
```sql
PRINT 'palabras' FROM BEGINNING;
```

Sal con **Control-C**.

---

## Crear un Stream en KSQL
```sql
CREATE STREAM palabras_stream
  (palabra VARCHAR)
   WITH (KAFKA_TOPIC='palabras',
        VALUE_FORMAT='DELIMITED');
```

---

## Consultas en el Stream
Selecciona todas las palabras y muestra su longitud:
```sql
SELECT palabra, LEN(palabra) FROM palabras_stream EMIT CHANGES;
```

Filtra palabras con longitud mayor a 7:
```sql
SELECT palabra AS mi_palabra, LEN(palabra) AS longitud FROM palabras_stream WHERE LEN(palabra) > 7 EMIT CHANGES;
```

### Ejercicio propio
Filtra palabras con longitud mayor a 10.

---

## Filtrar palabras que empiezan por "t"
```sql
SELECT palabra
FROM palabras_stream
WHERE palabra LIKE 't%' EMIT CHANGES;
```

### Ejercicio propio
Filtra palabras que terminan con "go".

---

## Crear una KTable para contar ocurrencias
```sql
CREATE TABLE mi_ktable AS
SELECT palabra,
       COUNT(*)
FROM palabras_stream
GROUP BY palabra
EMIT CHANGES;
```

Consultar la KTable:
```sql
SELECT * FROM mi_ktable EMIT CHANGES;
```

---

### Más ejercicios
**Ejercicio 5.1**
Encuentra palabras que empiecen con "ca", terminen con "o" y tengan más de 6 caracteres.

**Ejercicio 5.2**
Selecciona todas las palabras en mayúsculas usando `UCASE(...)`.

**Ejercicio 5.3 (Avanzado)**
Consulta la documentación oficial para más funciones:
[https://docs.confluent.io/current/ksql/docs/developer-guide/syntax-reference.html](https://docs.confluent.io/current/ksql/docs/developer-guide/syntax-reference.html)
