## **Objetivo del ejercicio**
- Entender explicaciones detalladas sobre Kafka, KSQL, Streams y KTables.
- Pasos para levantar el entorno con Docker.
- Cómo crear topics y producir mensajes desde Python.
- Consultas en KSQL.
- Ejemplos prácticos para filtrar datos y escribir en nuevos topics.

---

## Levantar el entorno Kafka con Docker
Necesitamos 4 servicios:
- **Zookeeper**: coordina los brokers de Kafka.
- **Kafka Broker**: almacena y distribuye los mensajes.
- **KSQL Server**: permite ejecutar consultas SQL sobre datos en Kafka.
- **KSQL CLI**: herramienta para interactuar con KSQL desde la terminal.

### ¿Por qué necesitamos estos componentes?
- Kafka por sí solo maneja mensajes, pero no entiende SQL.
- KSQL añade una capa que permite consultar datos en tiempo real usando sintaxis SQL.

### Pasos:
2. Ejecuta:
   ```bash
   docker-compose up -d
   ```
   Esto descargará las imágenes y levantará los contenedores.

**¿Cómo comprobar que todo está funcionando?**
```bash
docker ps
```
Debes ver los contenedores `zookeeper`, `kafka`, `ksql`, y `ksql-cli` en estado **Up**.

---

## **2. Crear un nuevo topic en Kafka**
Un *topic* es un espacio donde se almacenan los mensajes. Kafka organiza los datos en topics, y cada topic puede tener varias particiones.

Ejecuta:
```bash
docker-compose exec kafka kafka-topics --create   --topic palabras   --partitions 1   --replication-factor 1   --if-not-exists   --bootstrap-server localhost:9092
```

**Explicación:**
- `--topic palabras`: nombre del topic.
- `--partitions 1`: número de particiones (para este ejercicio, 1 es suficiente).
- `--replication-factor 1`: cuántas copias del topic se guardan (1 porque solo tenemos un broker).
- `--bootstrap-server localhost:9092`: dirección del broker.

---

## **3. Ejecutar el productor en Python**
Este productor leerá frases del libro *El Quijote* y enviará cada palabra al topic `palabras`.

Pasos:
1. Abre Visual Studio Code.
2. Ejecuta el archivo `ejercicio_8_ksql/producer.py`.
3. Este script:
   - Lee el archivo `el_quijote_book.txt` línea por línea.
   - Separa las palabras de cada frase.
   - Envía cada palabra suelta como un mensaje a Kafka.

**¿Cómo comprobar que funciona?**
```bash
docker-compose exec kafka kafka-console-consumer   --topic palabras   --from-beginning   --bootstrap-server localhost:9092
```
Si ves palabras llegando, ¡todo está correcto! Sal con **Ctrl+C**.

---

## **4. Abrir KSQL en la consola**
Ejecuta:
```bash
docker-compose exec ksql-cli ksql http://ksql:8088
```

**¿Qué hace esto?**
- Abre la CLI de KSQL.
- Se conecta al servidor KSQL en el puerto 8088.

Si todo va bien, verás el banner de KSQL.

---

## **5. Consultar los mensajes con KSQL**
Primero, ajusta el offset para leer desde el principio:
```sql
SET 'auto.offset.reset' = 'earliest';
```

Ver los topics disponibles:
```sql
SHOW TOPICS;
```
Debes ver `palabras`.

Imprimir los mensajes:
```sql
PRINT 'palabras' FROM BEGINNING;
```
Esto muestra los mensajes tal cual se enviaron.

---

## **6. Crear un Stream en KSQL**
### ¿Qué es un Stream?
Un **Stream** en KSQL es una representación lógica de los datos que fluyen en tiempo real desde un topic de Kafka. **No es un topic nuevo**, sino una vista sobre un topic existente. Cada mensaje que llega al topic se refleja en el Stream.

**Diferencias entre Stream y Topic:**
- El **topic** es el almacenamiento físico de los mensajes.
- El **Stream** es una abstracción que permite consultar esos mensajes con SQL.

Cuando creas un Stream, KSQL no crea un topic adicional (a menos que hagas operaciones que generen resultados en otro Stream o Table). Simplemente define cómo interpretar los datos del topic.

```sql
CREATE STREAM palabras_stream
  (palabra VARCHAR)
   WITH (KAFKA_TOPIC='palabras',
        VALUE_FORMAT='DELIMITED');
```

**Explicación:**
- `palabra VARCHAR`: cada mensaje será interpretado como una columna llamada `palabra`.
- `KAFKA_TOPIC='palabras'`: el stream se alimenta del topic `palabras`.
- `VALUE_FORMAT='DELIMITED'`: formato simple (cada mensaje es una palabra).

---

## **7. Consultas en el Stream**
Ejemplo: mostrar cada palabra y su longitud:
```sql
SELECT palabra, LEN(palabra) FROM palabras_stream EMIT CHANGES;
```


### ¿Qué hace EMIT CHANGES?
- En KSQL, las consultas sobre Streams son continuas porque los Streams no tienen fin.
- EMIT CHANGES indica que la consulta debe mostrar resultados en tiempo real cada vez que llegue un nuevo mensaje que cumpla la condición.
- Sin esta cláusula, la consulta sería interpretada como estática (snapshot), lo cual no está permitido sobre Streams.


---

Filtrar palabras con más de 7 caracteres:
```sql
SELECT palabra AS mi_palabra, LEN(palabra) AS longitud
FROM palabras_stream
WHERE LEN(palabra) > 7 EMIT CHANGES;
```

**Ejercicio propio:** Filtra palabras con longitud mayor a 10.

---

## **8. Ejemplo Consultas con patrones**
Filtrar palabras que empiezan por "t":
```sql
SELECT palabra
FROM palabras_stream
WHERE palabra LIKE 't%' EMIT CHANGES;
```

**Ejercicio propio:** Filtra palabras que terminan con "lo":

**Ejercicio propio:** Filtra palabras que empiezen con "c" terminan con "o" y sean de longitud mayor a 5:


---

## **9. Crear una KTable para contar ocurrencias**
### ¿Qué es una KTable?
Una **KTable** es similar a una tabla en una base de datos, pero representa el estado agregado de los datos. Mientras que un Stream refleja eventos en tiempo real, una KTable mantiene el último valor por clave.

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
Encuentra palabras que empiecen con "c", terminen con "o" y tengan más de 4 caracteres.

**Ejercicio 5.2**
Selecciona todas las palabras en mayúsculas usando `UCASE(...)`.

**Ejercicio 5.3 (Avanzado)**
Consulta la documentación oficial para más funciones:
[https://docs.confluent.io/current/ksql/docs/developer-guide/syntax-reference.html](https://docs.confluent.io/current/ksql/docs/developer-guide/syntax-reference.html)

---



---

# Escribir/INSERTAR en nuevos topics con KSQL  (una especie de SQL insert o equivalente a un Python Kafka Producer)

## **Ejemplo 1: Filtrar palabras largas y escribir en un nuevo topic**

Ya tenemos un topic llamado `palabras` que contiene palabras del libro *El Quijote*.
Y también tenemos el STREAM `palabras_stream`


### **Paso 2: Crear un nuevo Stream con palabras largas**
Queremos filtrar palabras con más de 8 caracteres y enviarlas a un nuevo topic llamado `palabras_largas`.

```sql
CREATE STREAM palabras_largas_stream WITH (
  KAFKA_TOPIC='palabras_largas',
  VALUE_FORMAT='DELIMITED'
) AS
SELECT palabra
FROM palabras_stream
WHERE LEN(palabra) > 8
EMIT CHANGES;
```

Comprobar el nuevo topic:
```sql
PRINT 'palabras_largas' FROM BEGINNING;
```

---

## **Ejemplo 2: Filtrar palabras que empiezan con "a" y escribir en otro topic**
```sql
CREATE STREAM palabras_a_stream WITH (
  KAFKA_TOPIC='palabras_a',
  VALUE_FORMAT='DELIMITED'
) AS
SELECT palabra
FROM palabras_stream
WHERE palabra LIKE 'a%'
EMIT CHANGES;
```

Comprobar el nuevo topic:
```sql
PRINT 'palabras_a' FROM BEGINNING;
```

---

## **Ejercicio propuesto**
Crea un nuevo Stream y topic llamado `palabras_cortas` que contenga palabras con menos de 4 caracteres y que empiezen por `t`.


---

### Conceptos clave:
- **CREATE STREAM ... AS SELECT**: permite crear un nuevo stream y topic a partir de una consulta.
- Cada vez que usamos esta sintaxis, KSQL crea automáticamente el nuevo topic indicado en `KAFKA_TOPIC`.
- Los filtros se aplican en tiempo real: solo los mensajes que cumplen la condición se insertan en el nuevo topic.

---

## **¿Qué ocurre cuando usamos CREATE STREAM ... AS SELECT?**

Cuando ejecutas una sentencia como:
```sql
CREATE STREAM palabras_largas_stream WITH (
  KAFKA_TOPIC='palabras_largas',
  VALUE_FORMAT='DELIMITED'
) AS
SELECT palabra
FROM palabras_stream
WHERE LEN(palabra) > 8
EMIT CHANGES;
```

### **¿Se crea un topic nuevo?**
Sí. Esta sintaxis **crea un nuevo topic físico en Kafka** con el nombre indicado en `KAFKA_TOPIC` (en este caso, `palabras_largas`). Además:
- El nuevo Stream (`palabras_largas_stream`) es una vista lógica sobre ese topic recién creado.
- Cada mensaje que cumpla la condición `LEN(palabra) > 8` se insertará en el topic `palabras_largas`.

### **Diferencia con CREATE STREAM normal:**
- `CREATE STREAM ... WITH (...)` sin `AS SELECT`: solo define una vista lógica sobre un topic existente (no crea un topic nuevo).
- `CREATE STREAM ... AS SELECT`: **crea un nuevo topic y lo llena con los resultados de la consulta**.

### **Visualización del flujo:**
```
Topic original (palabras) --> Stream lógico (palabras_stream) --> Filtro --> Nuevo topic físico (palabras_largas) --> Nuevo Stream lógico (palabras_largas_stream)
```

Este patrón es muy útil para crear pipelines de datos en tiempo real, donde cada paso genera un topic con datos transformados.
