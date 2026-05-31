-- queries.sql (FINAL VERSION)

-- 1. Configuración para leer desde el principio
SET 'auto.offset.reset' = 'earliest';

-- 2. Crear el STREAM (Lectura de datos limpios)
CREATE STREAM clean_stream (
    cliente VARCHAR, 
    categoria VARCHAR, 
    monto DOUBLE,
    procesado_por VARCHAR
) WITH (
    KAFKA_TOPIC='clean-transactions', 
    VALUE_FORMAT='JSON',
    PARTITIONS=1
);

-- 3. Crear la TABLA (Agregación de negocio)
CREATE TABLE ventas_stats AS
SELECT 
    categoria, 
    COUNT(*) AS total_pedidos, 
    -- Usamos CAST para redondear a 2 decimales
    CAST(SUM(monto) AS DECIMAL(10,2)) AS total_ingresos
FROM clean_stream
GROUP BY categoria
EMIT CHANGES;