--- Stream con los datos del producer temperatura_Valencia
CREATE STREAM temperatura_Valencia_stream (
    ciudad VARCHAR,
    fecha VARCHAR,
    hora VARCHAR,
    temperatura DOUBLE
) WITH (
    KAFKA_TOPIC='temperatura_Valencia',
    VALUE_FORMAT='JSON'
);

--- Comprobar que ha importado bien los datos
SELECT *
FROM temperatura_Valencia_stream
WHERE ciudad = 'Valencia' EMIT CHANGES;

--- Calcular la media de hoy y guardarla en una tabla para luego generar el stream
CREATE TABLE temperatura_Valencia_media_tb WITH (
    KAFKA_TOPIC='temperatura_Valencia_media',
    VALUE_FORMAT='DELIMITED'
) AS
SELECT fecha AS fecha, AVG(temperatura) AS temperatura_media
FROM temperatura_Valencia_stream
WHERE fecha = TIMESTAMPTOSTRING(ROWTIME, 'yyyy-MM-dd')
GROUP BY fecha
EMIT CHANGES;

--- Stream temperatura_Valencia_media_stream con los datos resultantes
CREATE STREAM temperatura_Valencia_media_stream (
    fecha VARCHAR,
    temperatura_media DOUBLE
) WITH (
    KAFKA_TOPIC='temperatura_Valencia_media',
    VALUE_FORMAT='DELIMITED',
    KEY_FORMAT='JSON'
);