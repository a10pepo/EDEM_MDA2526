{{ config(materialized='view') }}

WITH staging AS (
    SELECT * FROM {{ ref('stg_valenbisi') }}
),

enriched AS (
    SELECT
        record_id,
        station_id,
        station_name,
        latitude,
        longitude,
        available_bikes,
        available_slots,
        station_status,
        total_capacity,
        updated_at,
        ROUND(
            (available_bikes::numeric / NULLIF(total_capacity, 0)) * 100, 
            2
        ) AS occupation_pct,
        DATE(updated_at) AS metric_date,
        EXTRACT(HOUR FROM updated_at) AS metric_hour

    FROM staging
    WHERE total_capacity > 0
)

SELECT * FROM enriched