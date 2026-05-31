# Ejercicio: Consumidor Kafka en Python

## Objetivo

Aprender a leer mensajes desde un tópico de Kafka usando Python y la librería `confluent_kafka`. Este ejercicio permite entender cómo funciona la suscripción a un tópico, la lectura de mensajes y cómo personalizar el comportamiento del consumidor.

---

## Requisitos

- Tener Kafka y Zookeeper en ejecución (puedes usar Docker Compose).
- Tener Python instalado.
- Instalar la librería necesaria:

```bash
pip install confluent-kafka
```

---

## Pasos para realizar el ejercicio

1. **Revisa el código del consumidor**:
   - Observa cómo se configura el consumidor (`bootstrap.servers`, `group.id`, `auto.offset.reset`).
   - Fíjate en cómo se suscribe al tópico y cómo lee los mensajes.

2. **Ejecuta el código**:
   - Guarda el script en un archivo, por ejemplo: `consumer.py`.
   - Ejecuta el script:

```bash
python consumer.py
```

3. **Observa la salida**:
   - Verás en la consola los mensajes que se están recibiendo.
   - Cada mensaje se muestra en texto legible (convertido desde bytes).

---

## Conceptos importantes

- **auto.offset.reset**:
  - `earliest`: lee todos los mensajes desde el principio del tópico.
  - `latest`: lee solo los mensajes nuevos que lleguen después de conectarse.
  - `none`: error si no hay posición guardada.

- **poll(1.0)**:
  - Espera hasta 1 segundo por un mensaje.
  - Si no llega nada en ese tiempo, devuelve `None`.
  - Puedes cambiar el valor para ajustar la frecuencia de lectura.

- **try / while True / except / finally**:
  - `try`: bloque principal donde se ejecuta la lógica.
  - `while True`: bucle infinito para seguir leyendo mensajes.
  - `except KeyboardInterrupt`: captura Ctrl+C para detener el programa.
  - `finally`: asegura cerrar el consumidor siempre.

---

## Ejercicios extra

1. **Cambia el valor de auto.offset.reset**:
   - Prueba con `latest` para leer solo mensajes nuevos.

2. **Modifica el tiempo de espera en poll()**:
   - Cambia `poll(1.0)` por `poll(0.5)` o `poll(2.0)` y observa el comportamiento.

3. **Filtra mensajes por contenido**:
   - Muestra solo los mensajes que contengan la palabra "Aprobado".

4 **Cuenta mensajes recibidos**:
   - Añade un contador para saber cuántos mensajes se han leído.

---

## Objetivo final

Comprender cómo funciona un consumidor Kafka, cómo se leen mensajes y cómo personalizar el flujo para casos reales.
