-- Definición del stream principal
CREATE STREAM sensor_stream (
    "sensor_id" VARCHAR,
    "value" DOUBLE,
    "temperature" DOUBLE,
    "humidity" DOUBLE,
    "status" VARCHAR,
    "timestamp" DOUBLE,
    "uuid" VARCHAR
) WITH (
    KAFKA_TOPIC='SENSOR_FAILURES_2',
    VALUE_FORMAT='JSON'
);

-- Stream de solo alertas
CREATE STREAM SENSOR_FAILURES AS
SELECT "sensor_id", "temperature", "status", "uuid" FROM sensor_stream
WHERE "temperature" > 80.0 OR "status" = 'FAIL';