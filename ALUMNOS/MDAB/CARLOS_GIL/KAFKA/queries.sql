CREATE STREAM ventas_stream (id_venta INT, cliente VARCHAR, modelo VARCHAR, precio INT) 
WITH (KAFKA_TOPIC='compras_raw', VALUE_FORMAT='JSON');

--filtrar ventas > 50000
CREATE STREAM ventas_high_value AS 
SELECT * FROM ventas_stream WHERE precio > 50000;