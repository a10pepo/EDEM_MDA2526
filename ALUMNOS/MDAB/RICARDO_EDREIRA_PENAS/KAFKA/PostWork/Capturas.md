## Producer
Se envian los 20 pedidos del archivo pedidos.txt al topic `pedidos`, uno por segundo.
![alt text](image.png)

## Consumer Processor
Lee del topic `pedidos`, descarta los pendientes (PED-004, PED-009, PED-017) y calcula el total de los confirmados. Los envia al topic `pedidos_procesados`.
![alt text](image-1.png)

## Consultas KSQL
Se crea un stream sobre `pedidos_procesados` y se filtra por total > 20 EUR.

`SELECT * FROM pedidos_stream EMIT CHANGES;` - muestra todos los pedidos procesados:
![alt text](image-2.png)

`SELECT * FROM pedidos_caros EMIT CHANGES;` - muestra solo los pedidos de mas de 20 EUR:
![alt text](image-3.png)

## Consumer Final
Lee del topic `PEDIDOS_CAROS` (creado por KSQL) y muestra los 4 pedidos caros por pantalla.
![alt text](image-4.png)
