{{ config(materialized='table') }}

WITH enriched_data AS (
    SELECT * FROM {{ ref('intermediate_valenbisi') }}
),

hourly_agg AS (
    SELECT
        station_id,
        station_name,
        metric_date,
        metric_hour,
        
        ROUND(AVG(available_bikes), 1) AS avg_bikes,
        MIN(available_bikes) AS min_bikes,
        
        ROUND(AVG(occupation_pct), 2) AS avg_occupation_pct,
        MAX(occupation_pct) AS max_occupation_pct,
        
        COUNT(*) AS readings_count

    FROM enriched_data
    GROUP BY 
        station_id, 
        station_name, 
        metric_date, 
        metric_hour
)

SELECT * FROM hourly_agg
ORDER BY metric_date DESC, metric_hour DESC, station_id