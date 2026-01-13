WITH source AS (
    -- Referenciamos la tabla raw que creaste en la Fase 1
    -- "source" es una buena práctica, pero por simplicidad usamos el nombre directo aquí
    SELECT * FROM valenbisi_raw
),

cleaned AS (
    SELECT
        id,
        station_id,
        station_name,
        latitude,
        longitude,
        available_bikes,
        available_slots,
        total_capacity,
        station_status,
        timestamp,
        -- CREAMOS COLUMNAS NUEVAS PARA FACILITAR EL ANÁLISIS:
        -- 1. Extraemos solo la fecha (Ej: 2024-01-20)
        CAST(timestamp AS DATE) as report_date,
        -- 2. Extraemos la hora del día (Ej: 9, 10, 11...)
        EXTRACT(HOUR FROM timestamp) as report_hour
    FROM source
)

SELECT * FROM cleaned