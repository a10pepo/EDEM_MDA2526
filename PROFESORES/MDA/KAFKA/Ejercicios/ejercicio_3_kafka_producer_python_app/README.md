# Ejercicio: Productor Kafka en Python

## Objetivo

Aprender a enviar mensajes a un tópico de Kafka usando Python y la librería `confluent_kafka`. Este ejercicio simula un flujo de datos en tiempo real, como actualizaciones de proyectos empresariales.

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

1. **Revisa el código del productor**:
   - Observa cómo se configura el productor (`bootstrap.servers` y `client.id`).
   - Fíjate en cómo se define el tópico y se envían los mensajes.

2. **Ejecuta el código**:
   - Guarda el script en un archivo, por ejemplo: `producer.py`.
   - Ejecuta el script:

```bash
python producer.py
```

3. **Observa la salida**:
   - Verás en la consola los mensajes que se están enviando.
   - Cada mensaje simula datos de negocio (proyecto, presupuesto, estado).

4. **Comprueba en Kafka**:
   - Si tienes un consumidor, ejecútalo para ver los mensajes recibidos.

---

## Ejercicios extra

1. **Cambia el nombre del tópico**:
   - Modifica la variable `topic_kafka` en el código.
   - Usa nombres creativos como `ventas_globales`, `marketing2025` o `alertas_stock`.

2. **Modifica el contenido de los mensajes**:
   - Cambia el diccionario `data` para enviar información diferente.
   - Ejemplo: pedidos internacionales, campañas de marketing, alertas de inventario.

3. **Ajusta el intervalo de tiempo**:
   - Cambia el valor en `time.sleep(1)`.
   - Prueba con `0.5` para mensajes más rápidos o `2` para más lentos.

4. **Envía más o menos mensajes**:
   - Cambia el rango del bucle `for e in range(100)`.
   - Por ejemplo, `range(10)` para menos mensajes.

5. **Añade una lógica condicional**:
   - Envía mensajes diferentes según el índice.
   - Ejemplo: si `e` es par, estado = "Aprobado"; si es impar, estado = "Pendiente".

---

## Objetivo final

Comprender cómo funciona un productor Kafka, cómo se envían mensajes y cómo personalizar el flujo para casos reales.
