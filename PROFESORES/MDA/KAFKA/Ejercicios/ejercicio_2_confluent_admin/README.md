# Clase Práctica: Introducción a Kafka

## Objetivos

1. Iniciar Kafka y Zookeeper usando Docker Compose.
2. Crear un tópico en Kafka llamado `ventas2025`.
3. Enviar mensajes desde la consola.
4. Ver mensajes en la interfaz web.
5. Enviar mensajes desde la interfaz web y verlos en la consola.

---


## Acceso a la Interfaz Web

Abre tu navegador y accede a:

[http://localhost:9021](http://localhost:9021)

Aquí podrás ver los tópicos y enviar mensajes.

---

## Actividades

### 1) Crear un Tópico

Desde la consola, crea un tópico llamado `ventas2025`:

```sh
docker-compose exec kafka kafka-topics --create --topic ventas2025 --bootstrap-server localhost:9092
```

### 2) Enviar Mensajes desde la Consola

Produce mensajes relacionados con ventas o proyectos:

```sh
docker-compose exec kafka kafka-console-producer --topic ventas2025 --broker-list localhost:9092
```

```
Pedido #101: 500 unidades
Proyecto Innovación: aprobado
Cliente ABC: pago recibido
Presupuesto Q4: 120000 EUR
Informe semanal: completado
Reunión con proveedor: confirmada
etc....
```

### 3) Ver Mensajes en la UI

En la interfaz web, busca el tópico `ventas2025` y revisa los mensajes enviados.

### 4) Enviar Mensajes desde la UI

En la UI, selecciona el tópico `ventas2025` y usa la opción **Produce a message** para enviar mensajes como:

```
Cliente XYZ: compra confirmada
Informe trimestral: listo
Pedido #202: 300 unidades
Nueva campaña marketing: lanzada
etc....
```

### 5) Ver Mensajes en la Consola

Abre otra terminal y ejecuta:

```sh
docker-compose exec kafka kafka-console-consumer --topic ventas2025 --from-beginning --bootstrap-server localhost:9092
```

Verás los mensajes enviados desde la consola y la UI.
