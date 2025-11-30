-- ============================================================================
-- Script de configuración ksqlDB
-- Proyecto: Tarea_Pacientes_Hospital
--
-- Cómo usar este script:
--   1) Entrar al contenedor del CLI:
--        docker exec -it ksql-cli /bin/sh
--   2) Lanzar el cliente:
--        ksql http://ksql:8088
--   3) Copiar y pegar, por bloques, los comandos que necesites.
--      (No hace falta ejecutarlo todo cada vez si ya has creado los streams)
-- ============================================================================


-- ============================================================================
-- 0. Comandos de inspección (opcionales)
-- ============================================================================

-- Ver streams definidos en ksqlDB
-- SHOW STREAMS;

-- Ver queries persistentes en ejecución
-- SHOW QUERIES;

-- Ver topics disponibles en el cluster Kafka
-- SHOW TOPICS;



-- ============================================================================
-- 1. Limpieza opcional de streams anteriores
--    (Úsalos solo si has estado probando cosas y quieres empezar de cero)
-- ============================================================================

DROP STREAM IF EXISTS ALERTAS_SEGUIMIENTO;
DROP STREAM IF EXISTS ALERTAS_PLANTA;
DROP STREAM IF EXISTS ALERTAS_UCI;
DROP STREAM IF EXISTS ALERTAS_PACIENTES;
DROP STREAM IF EXISTS SIGNOS_VITALES_ENRIQUECIDOS;



-- ============================================================================
-- 2. Stream base sobre el topic enriquecido
--    Fuente: topic "signos_vitales_enriquecidos" producido por
--    consumidor_enriquecedor.py
-- ============================================================================

CREATE STREAM SIGNOS_VITALES_ENRIQUECIDOS (
  paciente_id        VARCHAR KEY,
  habitacion         VARCHAR,
  edad               INT,
  diagnostico_base   VARCHAR,
  frecuencia_cardiaca DOUBLE,
  tension_sistolica  DOUBLE,
  tension_diastolica DOUBLE,
  saturacion_oxigeno DOUBLE,
  temperatura        DOUBLE,
  "timestamp"        VARCHAR,
  segmento_paciente  VARCHAR,
  estado_clinico     VARCHAR,
  prioridad_atencion VARCHAR
) WITH (
  KAFKA_TOPIC = 'signos_vitales_enriquecidos',
  VALUE_FORMAT = 'JSON',
  PARTITIONS = 1
);



-- ============================================================================
-- 3. Stream de alertas globales
--    Genera el topic "alertas_pacientes_topic" a partir de los datos
--    enriquecidos, filtrando solo pacientes relevantes.
-- ============================================================================
-- Regla:
--   - Se genera alerta cuando:
--       * estado_clinico != 'ESTABLE'
--         (CRITICO o ALERTA)
--       O
--       * segmento_paciente = 'ALTO_RIESGO'
--         y prioridad_atencion != 'NORMAL'
-- ============================================================================

CREATE STREAM ALERTAS_PACIENTES
WITH (
  KAFKA_TOPIC = 'alertas_pacientes_topic',
  VALUE_FORMAT = 'JSON',
  PARTITIONS = 1
) AS
SELECT
  paciente_id,
  habitacion,
  edad,
  diagnostico_base,
  frecuencia_cardiaca,
  tension_sistolica,
  tension_diastolica,
  saturacion_oxigeno,
  temperatura,
  "timestamp",
  segmento_paciente,
  estado_clinico,
  prioridad_atencion
FROM SIGNOS_VITALES_ENRIQUECIDOS
WHERE
  estado_clinico != 'ESTABLE'
  OR (segmento_paciente = 'ALTO_RIESGO' AND prioridad_atencion != 'NORMAL')
EMIT CHANGES;



-- ============================================================================
-- 4. Streams derivados por equipo asistencial
--    A partir de ALERTAS_PACIENTES, se enrutan las alertas a distintos
--    equipos del hospital usando varios topics independientes.
-- ============================================================================


-- 4.1. Alertas para UCI
--      - Recibe pacientes críticos o con prioridad MUY_ALTA
--      - Topic: alertas_uci_topic
--      - Consumer: consumidor_alertas_uci.py
-- ============================================================================

CREATE STREAM ALERTAS_UCI
WITH (
  KAFKA_TOPIC = 'alertas_uci_topic',
  VALUE_FORMAT = 'JSON',
  PARTITIONS = 1
) AS
SELECT *
FROM ALERTAS_PACIENTES
WHERE ESTADO_CLINICO = 'CRITICO'
   OR PRIORIDAD_ATENCION = 'MUY_ALTA'
EMIT CHANGES;



-- 4.2. Alertas para Planta
--      - Recibe pacientes en ALERTA y de ALTO_RIESGO
--      - Topic: alertas_planta_topic
--      - Consumer: consumidor_alertas_planta.py
-- ============================================================================

CREATE STREAM ALERTAS_PLANTA
WITH (
  KAFKA_TOPIC = 'alertas_planta_topic',
  VALUE_FORMAT = 'JSON',
  PARTITIONS = 1
) AS
SELECT *
FROM ALERTAS_PACIENTES
WHERE ESTADO_CLINICO = 'ALERTA'
  AND SEGMENTO_PACIENTE = 'ALTO_RIESGO'
EMIT CHANGES;



-- 4.3. Alertas para Seguimiento
--      - Recibe pacientes ESTABLES pero de ALTO_RIESGO
--      - Topic: alertas_seguimiento_topic
--      - Consumer: consumidor_alertas_seguimiento.py
-- ============================================================================

CREATE STREAM ALERTAS_SEGUIMIENTO
WITH (
  KAFKA_TOPIC = 'alertas_seguimiento_topic',
  VALUE_FORMAT = 'JSON',
  PARTITIONS = 1
) AS
SELECT *
FROM ALERTAS_PACIENTES
WHERE ESTADO_CLINICO = 'ESTABLE'
  AND SEGMENTO_PACIENTE = 'ALTO_RIESGO'
EMIT CHANGES;



-- ============================================================================
-- 5. Consultas de comprobación (para usar desde el CLI de ksqlDB)
-- ============================================================================

-- Ver todos los streams definidos
-- SHOW STREAMS;

-- Ver las queries persistentes asociadas a los streams "AS SELECT"
-- SHOW QUERIES;

-- Ver una muestra de registros enriquecidos
-- (ejecutar mientras se lanza el productor)
-- SELECT * FROM SIGNOS_VITALES_ENRIQUECIDOS EMIT CHANGES LIMIT 5;

-- Ver una muestra de alertas globales
-- SELECT * FROM ALERTAS_PACIENTES EMIT CHANGES LIMIT 5;

-- Ver ejemplos de alertas por equipo
-- SELECT * FROM ALERTAS_UCI EMIT CHANGES LIMIT 5;
-- SELECT * FROM ALERTAS_PLANTA EMIT CHANGES LIMIT 5;
-- SELECT * FROM ALERTAS_SEGUIMIENTO EMIT CHANGES LIMIT 5;
