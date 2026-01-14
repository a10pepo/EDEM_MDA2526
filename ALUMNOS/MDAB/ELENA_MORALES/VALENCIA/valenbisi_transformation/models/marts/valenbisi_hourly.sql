-- Usamos {{ ref('...') }} para que dbt sepa que este modelo depende del anterior
SELECT
    station_id,
    station_name,
    report_date,
    report_hour,
    -- Calculamos métricas:
    ROUND(AVG(available_bikes), 2) as avg_available_bikes,
    MIN(available_bikes) as min_available_bikes, -- ¿Llegó a estar vacía?
    MAX(available_bikes) as max_available_bikes
FROM {{ ref('stg_valenbisi') }}
GROUP BY 1, 2, 3, 4