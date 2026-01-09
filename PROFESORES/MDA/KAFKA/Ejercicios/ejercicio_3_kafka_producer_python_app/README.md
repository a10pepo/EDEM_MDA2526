# Ejercicio: Productor Kafka en Python

## Objetivo

Aprender a enviar mensajes a un tópico de Kafka usando Python y la librería `confluent_kafka`. Este ejercicio simula un flujo de datos en tiempo real, como actualizaciones de proyectos empresariales.

Comprender cómo funciona un productor Kafka, cómo se envían mensajes y cómo personalizar el flujo para casos reales.
---

## Requisitos
Instalar la librería necesaria:

```bash
pip install confluent-kafka
```

---

## Pasos para realizar el ejercicio

1. **Revisa el código del productor**:
   - Ya tienes una app Python de un Kafka Producer en `producer.py`
   - Observa cómo se configura el productor (`bootstrap.servers` y `client.id`).
   - Fíjate en cómo se define el tópico y se envían los mensajes.

2. **Ejecuta el código**:
   - Ejecuta el script `producer.py`:

Puedes lanzar el producer.py desde VisualEstudio o con el comando 'python producer.py' desde la terminal.
```bash
python producer.py
```


3. **Observa la salida**:
   - Abre una consola y observa los mensajes que se están enviando al topic `proyectos_innovacion`
   - Cada mensaje simula datos de negocio (proyecto, presupuesto, estado).
---

## Ejercicios extra

1. **Cambia el nombre del tópico**:
   - Modifica la variable `topic_kafka` en el código.
   - Usa nombres creativos como `ventas_globales`, `marketing2025` o `alertas_stock`.

2. **Modifica el contenido de los mensajes**:
   - Cambia el diccionario `data` para enviar información diferente.
   - Ejemplo: pedidos internacionales, campañas de marketing, alertas de inventario.

3. **Envía más o menos mensajes**:
   - Cambia el rango del bucle `for e in range(100)`.
   - Por ejemplo, `range(10)` para menos mensajes.

4. **Añade una lógica condicional**:
   - Envía mensajes diferentes según el índice.
   - Ejemplo: si `e` es par, estado = "Aprobado"; si es impar, estado = "Pendiente".

---
