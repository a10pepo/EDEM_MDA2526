### EXPLICACIÓN

## Caso de uso. Conjunto de datos seleccionado
https://api.waqi.info/ como API de proporción de datos con la intención de medir la temperatura de valencia periódicamente y calcular su media para indicar si ha hecho buen o mal tiempo dia a dia.

## Arquitectura final implementada
- producer.py - Lee la API y produce los datos
- consumer.py - Lee del producer los resultados y publica nuevos resultados
- KSQL.sql - Consultas para ejecución en KSQL

## Ejemplos JSON de su modelo JSON de datos
{"ciudad": "Valencia", "fecha": "YYYY-mm-dd", "hora": "HH:mm:ss", "temperatura": 00.0}

* Se incluyen capturas de pantalla de los diferentes pasos: 
1) la ingesta
2) el procesamiento con un consumidor
3) el procesamiento con KSQL y la impresión final en pantalla del resultado esperado.