El objetivo de esta aplicación es procesar transacciones bancarias de un E-commerce en tiempo real para cumplir con dos necesidades de negocio críticas:
Seguridad y Cumplimiento (GDPR): Los datos brutos contienen información sensible (números completos de tarjetas de crédito) y transacciones fallidas. Es necesario limpiar y anonimizar estos datos antes de que sean almacenados o analizados por otros departamentos.
Marketing en tiempo real (Detección VIP): El equipo de ventas necesita identificar instantáneamente las compras de alto valor (superiores a 500€) para disparar acciones de fidelización o alertas de seguridad preventivas.
La solución implementada ingesta datos brutos, los limpia mediante un procesador en Python, y utiliza KSQL para filtrar y detectar eventos de alto valor, entregando una alerta final en una terminal de monitoreo.

  ----- Dataset seleccionado -----
Para este ejercicio se ha utilizado un generador de datos sintéticos (script producer.py).
Este dataset simula un flujo continuo de transacciones financieras con los siguientes atributos:

- ID: Identificador único de la transacción.
- User: Nombre del cliente.
- Card: Número de tarjeta de crédito (16 dígitos).
- Amount: Monto de la transacción (numérico).
- Status: Estado del pago (Success, Failed, Cancelled).

El flujo de datos simula un entorno real con una mezcla de transacciones exitosas y erróneas.

----- Arquitectura implementada -----

La arquitectura sigue un patrón de pipeline ETL en Streaming:

1. Ingesta (Producer): Un script en Python genera transacciones aleatorias y las envía al tópico raw_transactions.
2. Procesamiento y Limpieza (Consumer/Producer): Un servicio intermedio en Python (python_cleaner.py) consume los datos brutos. Realiza dos acciones:
3. Filtrado: Descarta transacciones con estado "Failed" o "Cancelled".
4. Enmascaramiento: Oculta los primeros 12 dígitos de la tarjeta de crédito para cumplir con normativas de privacidad.
5. Reenvío: Publica los datos limpios en el tópico clean_transactions.
6. Análisis con KSQL: KSQLDB lee el tópico limpio y ejecuta una consulta continua (CREATE STREAM ... AS SELECT ... WHERE amount > 500). Esto filtra las ventas VIP y las escribe automáticamente en un tercer tópico: vip_large_transactions.
7. Visualización (Consumer Final): Un script final (final_monitor.py) escucha el tópico de alertas VIP y muestra en pantalla los eventos críticos para el negocio.

----- Ejemplos del modelo de datos (JSON) -----

A continuación, se muestra cómo evoluciona un mensaje a través del pipeline:

A. Mensaje Original (Raw Data)
Contiene datos sensibles y posibles errores.

JSON
{
  "id": "TX-1024",
  "user": "Alice",
  "card": "4500-1234-5678-9010",
  "amount": 120.50,
  "status": "Failed"
}

B. Mensaje Procesado (Clean Data)
Tarjeta enmascarada y solo transacciones exitosas.

JSON
{
  "id": "TX-1025",
  "user": "Bob",
  "card": "****-****-****-1122",
  "amount": 850.00,
  "status": "Success"
}

C. Mensaje Final (VIP Alert)
Filtrado por lógica de negocio (Monto > 500).

JSON
{
  "ID": "TX-1025",
  "USER": "Bob",
  "CARD": "****-****-****-1122",
  "AMOUNT": 850.00,
  "STATUS": "Success"
}