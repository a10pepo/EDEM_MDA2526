SELECT
    station_id,
    station_name,
    report_date,
    -- Métricas diarias
    ROUND(AVG(available_bikes), 2) as daily_avg_bikes,
    MIN(available_bikes) as daily_min_bikes,
    MAX(available_bikes) as daily_max_bikes
FROM {{ ref('stg_valenbisi') }}
GROUP BY 1, 2, 3