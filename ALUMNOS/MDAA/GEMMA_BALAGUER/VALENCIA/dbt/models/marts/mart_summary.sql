{{ config(
    materialized='table'
) }}

SELECT
    status,
    COUNT(*) AS num_stations,
    AVG(available) AS avg_bikes_available,
    AVG(free) AS avg_spaces_free,
    MAX(updated_at) AS last_update
FROM {{ ref('int_dispo') }}
GROUP BY status
ORDER BY status
