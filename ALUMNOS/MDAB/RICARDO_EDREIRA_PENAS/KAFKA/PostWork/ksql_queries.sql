-- Procesamiento de pedidos
-- docker exec -it ksql-cli ksql http://ksql:8088

-- Crear STREAM sobre el topic 'pedidos_procesados'
CREATE STREAM pedidos_stream (
    pedido_id VARCHAR,
    restaurante VARCHAR,
    plato VARCHAR,
    cantidad INT,
    precio DOUBLE,
    total DOUBLE,
    cliente VARCHAR,
    metodo_pago VARCHAR
) WITH (
    KAFKA_TOPIC = 'pedidos_procesados',
    VALUE_FORMAT = 'JSON'
);

-- Crear STREAM con pedidos que cuestan mas de 20 EUR
-- Se escribe automaticamente en el topic 'PEDIDOS_CAROS'
CREATE STREAM pedidos_caros AS
    SELECT pedido_id, restaurante, plato, total, cliente
    FROM pedidos_stream
    WHERE total > 20.0
    EMIT CHANGES;

-- Consultas:
-- SELECT * FROM pedidos_stream EMIT CHANGES;
-- SELECT * FROM pedidos_caros EMIT CHANGES;
