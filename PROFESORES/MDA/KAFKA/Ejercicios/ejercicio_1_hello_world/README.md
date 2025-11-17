# Kafka - Ejercicio 1

## ¿Qué es Kafka?
Kafka es una plataforma de mensajería distribuida que permite enviar y recibir datos en tiempo real entre aplicaciones.  
Piensa en Kafka como un **buzón gigante** donde:
- **Productores** crean y envian mensajes.
- **Consumidores** los leen.
- Los mensajes se organizan en **tópicos** (canales).

---

## Objetivos del laboratorio
1. Levantar Kafka y Zookeeper con Docker.
2. Comprobar que los servicios están funcionando.
3. Crear un tópico en Kafka.
4. Producir mensajes desde la línea de comandos.
5. Leer mensajes desde la línea de comandos.
6. Producir mensajes con claves.
7. Explorar la interfaz web de Kafka.
8. Describir el tópico creado.

---

## Requisitos previos
- Docker instalado.
- Todos los demás contenedores Docker detenidos.

---

## Conceptos clave
- **Broker**: Servidor Kafka que almacena mensajes.
- **Zookeeper**: Servicio que coordina los brokers (en versiones modernas se usa KRaft, pero aquí usamos Zookeeper).
- **Tópico**: Canal donde se publican mensajes.
- **Partición**: Divide el tópico en segmentos para paralelismo.
- **Replicación**: Copias para tolerancia a fallos.
- **Productor**: Envía mensajes.
- **Consumidor**: Lee mensajes.

---

## Diagrama conceptual
*(Productor (crea y envia mensajes a Kafka) → Tópico (canal de Kafka donde se guardan los mensajes) → Consumidor (lee los mensajes)*  


---

## Pasos del laboratorio

### 1) Levantar Kafka y Zookeeper
Escenario simple: 1 Zookeeper + 1 broker Kafka.

Abre una terminal, y ves a la ruta donde se encuentra el fichero KAFKA/docker-compose.yml

```sh
# Levantar los contenedores en segundo plano
docker-compose up -d
```

---

### 2) Comprobar el estado de los contenedores

```sh
docker-compose ps
```

Salida esperada:

```
Name                  Command            State           Ports
---------------------------------------------------------------------------
lab0_kafka_1       /etc/confluent/docker/run   Up      0.0.0.0:9092->9092/tcp
lab0_zookeeper_1   /etc/confluent/docker/run   Up      0.0.0.0:2181->2181/tcp
```

#### Verificar logs de Zookeeper:
```sh
# Windows
docker-compose logs zookeeper | findstr binding
# Linux / macOS
docker-compose logs zookeeper | grep -i binding
```

#### Verificar logs de Kafka:
```sh
# Windows
docker-compose logs kafka | findstr started
# Linux / macOS
docker-compose logs kafka | grep -i started
```

---

### 3) Crear un tópico en Kafka
```sh
docker-compose exec kafka kafka-topics   --create   --topic topicEdem   --partitions 1   --replication-factor 1   --if-not-exists   --bootstrap-server localhost:9092
```

Salida:
```
Created topic topicEdem.
```

---

### 4) Producir mensajes desde la línea de comandos
```sh
docker-compose exec kafka kafka-console-producer   --topic topicEdem   --broker-list localhost:9092
```

Escribe mensajes:
```
> hola
> kafka
> escribe y envía más mensajes, los que tú quieras...
```

---

### 5) Leer mensajes desde la línea de comandos
Abre una consola nueva, y mantén la consola del Producer abierta.
```sh
docker-compose exec kafka kafka-console-consumer   --topic topicEdem   --from-beginning   --bootstrap-server localhost:9092
```

Salida:
```
hola
kafka
```

---


## Ejercicios opcionales
1. Crea un segundo tópico llamado `students` y produce mensajes con nombres.
2. Abre dos consumidores que lean del topic `students` y observa cómo reciben los mensajes cuando los produces desde otra consola.
3. ¿Qué pasa si cambias `--from-beginning` por no ponerlo?

---

## Glosario rápido
- **Productor**: Envía mensajes.
- **Consumidor**: Lee mensajes.
- **Broker**: Servidor Kafka donde se guardan los mensajes producidos por el Productor, y desde donde los lee un Consumidor tantas veces como necesite.
- **Tópico**: Canal de mensajes.
- **Partición**: Subdivisión del tópico.
- **Replicación**: Copias para alta disponibilidad.Son copias de seguridad.
- **Zookeeper**: Coordina brokers Kafka. Es un componente puramente técnico y de soporte para que funcione Kafka.

