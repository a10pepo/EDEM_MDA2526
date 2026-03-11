-- ----------------------------
-- 1. General Settings
-- ----------------------------
SET 'auto.offset.reset' = 'earliest';

-- ============================================================
-- 1. STREAM fuente: lectura del tópico original
-- ============================================================
CREATE STREAM consumption_raw_stream (
  device_id INTEGER,
  totalConsumption INTEGER,
  timestamp DOUBLE
) WITH (
  KAFKA_TOPIC='inverter_data',
  VALUE_FORMAT='JSON'
);

-- ============================================================
-- 2. TABLE con el último totalConsumption por id
--    Esto mantiene el último valor procesado por cada id
-- ============================================================
CREATE TABLE last_consumption
  AS SELECT 
    device_id,
    LATEST_BY_OFFSET(totalConsumption) AS last_totalConsumption
  FROM consumption_raw_stream
  GROUP BY device_id;

-- ============================================================
-- 3. STREAM que une el valor nuevo con el antiguo
-- ============================================================
CREATE STREAM consumption_with_prev AS
  SELECT 
    s.device_id as device_id,
    s.totalConsumption as totalConsumption,
    t.last_totalConsumption AS prev_totalConsumption,
    s.timestamp as timestamp
  FROM consumption_raw_stream s
  LEFT JOIN last_consumption t
  ON s.device_id = t.device_id;

-- ============================================================
-- 4. STREAM de alertas cuando hay salto > 50 unidades
--    Se publica en el tópico "consumption_alerts"
-- ============================================================
CREATE STREAM consumption_alerts
  WITH (
    KAFKA_TOPIC='inverter_alerts',
    VALUE_FORMAT='JSON'
  ) AS
  SELECT
    device_id,
    totalConsumption,
    prev_totalConsumption,
    (totalConsumption - prev_totalConsumption) AS diff,
    timestamp
  FROM consumption_with_prev
  WHERE prev_totalConsumption IS NOT NULL
    AND (totalConsumption - prev_totalConsumption) > 50
    AND device_id IS NOT NULL
    AND totalConsumption IS NOT NULL
    AND prev_totalConsumption IS NOT NULL;

-- ============================================================
-- 6. CONSULTAR LAS ALERTAS
-- ============================================================
-- Ejecutar:
-- SELECT * FROM consumption_alerts EMIT CHANGES;
-- ============================================================
