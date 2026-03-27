--Creamos el stream vinculándolo al tópico que genera el script de Python
CREATE STREAM stream_alertas (
    order_id VARCHAR,
    porcentaje_rotura DOUBLE,
    nivel_criticidad VARCHAR,
    timestamp DOUBLE
) WITH (
    KAFKA_TOPIC='alertas_entregas',
    VALUE_FORMAT='JSON',
    TIMESTAMP='timestamp'
);

--Creamos un reporte agrupado: media de rotura por nivel de criticidad
--Esto se actualizará solo cada vez que llegue un mensaje
CREATE TABLE reporte_criticidad AS
    SELECT nivel_criticidad,
           COUNT(*) AS total_pedidos,
           AVG(porcentaje_rotura) AS rotura_media
    FROM stream_alertas
    GROUP BY nivel_criticidad
    EMIT CHANGES;