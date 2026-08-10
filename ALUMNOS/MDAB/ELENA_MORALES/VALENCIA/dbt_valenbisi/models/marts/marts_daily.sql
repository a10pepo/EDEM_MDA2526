{{ config(materialized='table') }}

WITH enriched_data AS (
    SELECT * FROM {{ ref('intermediate_valenbisi') }}
),

daily_agg AS (
    SELECT
        station_id,
        station_name,
        metric_date,
        
        ROUND(AVG(total_capacity), 0) AS capacity,
        ROUND(AVG(available_bikes), 1) AS avg_daily_bikes,
        ROUND(AVG(occupation_pct), 2) AS avg_daily_occupation,
        
        MAX(occupation_pct) AS max_occupation_reached,
        MIN(available_bikes) AS min_bikes_reached,
        
        -- Flags
        MAX(CASE WHEN available_bikes = 0 THEN 1 ELSE 0 END) AS was_empty_flag,
        MAX(CASE WHEN available_slots = 0 THEN 1 ELSE 0 END) AS was_full_flag

    FROM enriched_data
    GROUP BY 
        station_id, 
        station_name, 
        metric_date
)

SELECT * FROM daily_agg
ORDER BY metric_date DESC, avg_daily_occupation DESC