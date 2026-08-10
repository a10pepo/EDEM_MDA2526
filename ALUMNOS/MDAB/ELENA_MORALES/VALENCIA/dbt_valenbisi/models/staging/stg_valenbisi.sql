{{ config(materialized='view') }}

WITH source AS (
    SELECT * FROM {{ source('valenbisi_source', 'valenbisi_raw') }}
),

renamed AS (
    SELECT
        id AS record_id,
        station_id,
        station_name,
        CAST(latitude AS NUMERIC) AS latitude,
        CAST(longitude AS NUMERIC) AS longitude,
        CAST(available_bikes AS INTEGER) AS available_bikes,
        CAST(available_slots AS INTEGER) AS available_slots,
        station_status,
        CAST(total_capacity AS INTEGER) AS total_capacity,
        timestamp AS updated_at
    FROM source
)

SELECT * FROM renamed