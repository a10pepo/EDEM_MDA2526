# 🚀 HACKATHON: RECEIPT JOURNEY (On-Prem Edition)
**Duración Total:** 5 Horas  
**Stack Tecnológico:** Python (Flask), PostgreSQL, Kafka, Nginx (Dockerized)

---

## 📜 Introducción para el Equipo
Bienvenidos. Son el nuevo equipo de ingeniería backend de "Receipt Journey". Su misión es construir el núcleo de una aplicación de gestión de gastos corporativos.

**La Regla de Oro:** No queremos "código espagueti". Estamos construyendo una arquitectura orientada a eventos, escalable y lista para desplegarse en servidores propios (On-Premise).

El Product Owner (PO) liberará nuevos requerimientos cada 30 minutos. Deben priorizar funcionalidad y estabilidad.

---

## ⏰ 00:00 - 00:30 | Misión 1: El Cimiento
**Contexto:** Necesitamos la estructura básica. No podemos construir una casa sin cimientos.

**Requerimiento de Producto:**
1. Crear un repositorio y una estructura de proyecto Flask básica.
2. Definir un archivo `docker-compose.yml` inicial que levante, al menos, la base de datos **PostgreSQL**.
3. La aplicación debe conectar con la base de datos y arrancar sin errores.

**Tech Hints:**
* Usar `psycopg2-binary` o `SQLAlchemy`.
* Las credenciales de la DB deben estar en variables de entorno, no en el código.

---

## ⏰ 00:30 - 01:00 | Misión 2: El Modelo de Datos
**Contexto:** Necesitamos saber qué guardar. Un ticket no es solo una imagen.

**Requerimiento de Producto:**
Diseñar e implementar la tabla `tickets` en PostgreSQL. Debe ser capaz de guardar:
* Un ID único.
* La ruta del archivo (path) de la imagen.
* El estado del procesamiento (`PENDING`, `PROCESSED`, `ERROR`).
* Fecha de creación.

**Tech Hints:**
* Usar Flask-Migrate (Alembic) para crear la tabla. Nada de `CREATE TABLE` manuales.

---

## ⏰ 01:00 - 01:30 | Misión 3: Ingesta de Tickets (API)
**Contexto:** Los usuarios necesitan subir sus facturas.

**Requerimiento de Producto:**
Crear un Endpoint `POST /upload` en la API.
1. Recibe una imagen (formato multipart).
2. Guarda la imagen en una carpeta local (volumen de Docker).
3. Crea un registro en la base de datos con estado `PENDING`.
4. Devuelve un `201 Created` al usuario con el ID del ticket.

**Restricción:** ¡El endpoint debe ser rápido! No intenten procesar la imagen aquí. Solo guárdenla.

---

## ⏰ 01:30 - 02:00 | Misión 4: Desacople (Kafka Producer)
**Contexto:** Si 10,000 usuarios suben tickets a la vez, el servidor se va a caer si procesamos todo síncronamente. Necesitamos una cola.

**Requerimiento de Producto:**
Integrar **Apache Kafka** en el `docker-compose.yml`.
1. Cuando el usuario sube un ticket (Endpoint `POST /upload`), la API debe enviar un mensaje a un tópico de Kafka llamado `new_tickets`.
2. El mensaje debe contener el ID del ticket y la ruta de la imagen en JSON.

**Tech Hints:**
* Container bitnami/kafka o similar.
* Librería Python: `confluent-kafka` o `kafka-python`.

---

## ⏰ 02:00 - 02:30 | Misión 5: El Worker (Kafka Consumer)
**Contexto:** Alguien tiene que hacer el trabajo sucio de leer esos tickets.

**Requerimiento de Producto:**
Crear un servicio separado (un script Python `worker.py`) que corra en su propio contenedor.
1. Debe escuchar continuamente el tópico `new_tickets`.
2. Cuando llegue un mensaje, debe imprimir "Procesando ticket [ID]...".
3. Simular un proceso de 5 segundos (OCR fake) y actualizar el estado en la base de datos a `PROCESSED`.

---

## ⏰ 02:30 - 03:00 | Misión 6: Enriquecimiento (Simulación de IA)
**Contexto:** Para ver el mapa, necesitamos coordenadas. Como no tenemos un OCR real, vamos a "mockear" los datos.

**Requerimiento de Producto:**
Mejorar el `worker.py`. Al procesar el ticket:
1. Generar aleatoriamente (o extraer de un mock) datos de negocio:
    * **Monto total:** (ej. $45.00).
    * **Categoría:** (Comida, Transporte, Hotel).
    * **Ubicación:** Generar una Latitud/Longitud aleatoria dentro de su ciudad.
2. Guardar estos nuevos datos en la tabla `tickets` (hacer update de las columnas correspondientes).

---

## ⏰ 03:00 - 03:30 | Misión 7: La Galería (Querying)
**Contexto:** El usuario quiere ver qué ha subido.

**Requerimiento de Producto:**
Crear un Endpoint `GET /tickets`.
1. Debe devolver un JSON con la lista de tickets procesados.
2. Debe incluir la URL pública para ver la imagen.
3. El JSON debe incluir los metadatos (monto, fecha, estado).

**Tech Hints:**
* ¿Cómo va a servir Flask las imágenes estáticas? (Pista: Nginx en la misión final, por ahora usen `send_from_directory` o preparen la ruta).

---

## ⏰ 03:30 - 04:00 | Misión 8: Visualización Geoespacial
**Contexto:** "Ver en un mapa donde hice cada compra".

**Requerimiento de Producto:**
Refinar el Endpoint `GET /tickets` o crear uno nuevo `GET /tickets/map`.
1. La estructura de respuesta debe estar optimizada para un mapa.
2. Formato sugerido:
   ```json
   {
     "id": 1,
     "lat": 40.4167,
     "lng": -3.7037,
     "title": "Cena en Madrid - $45",
     "category": "Comida"
   }
