CREATE TABLE contar_señales AS
    SELECT 
        accion,
        señal,
        COUNT(*) AS total
    FROM stream_señales
    GROUP BY accion, señal
    EMIT CHANGES;