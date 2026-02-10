-- 1. Stream avanzado
CREATE STREAM music_stream_v3 (
    titulo VARCHAR,
    artista VARCHAR,
    pais VARCHAR,
    ip VARCHAR,
    dispositivo VARCHAR,
    es_bot BOOLEAN,
    duracion INT
) WITH (KAFKA_TOPIC='music_enriched_data', VALUE_FORMAT='JSON');

-- 2. Alerta de Seguridad: ¿Qué IPs están saturando el sistema?
-- Detectamos IPs que han hecho más de 5 peticiones en los últimos 30 segundos
CREATE TABLE alertas_fraude AS
    SELECT ip, COUNT(*) AS peticiones_sospechosas
    FROM music_stream_v3
    WINDOW TUMBLING (SIZE 30 SECONDS)
    GROUP BY ip
    HAVING COUNT(*) > 5;

-- 3. Métricas de Dispositivos (¿Desde dónde nos escuchan más?)
CREATE TABLE metricas_dispositivos AS
    SELECT dispositivo, COUNT(*) AS total
    FROM music_stream_v3
    GROUP BY dispositivo;