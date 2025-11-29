CREATE STREAM stream_señales (
    accion VARCHAR,
    señal VARCHAR,
    precio DOUBLE,
    ma20 DOUBLE,
    fecha VARCHAR,
    texto VARCHAR
) WITH (
    KAFKA_TOPIC='señales',
    VALUE_FORMAT='JSON'
);