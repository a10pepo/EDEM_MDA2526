-- rocket_performance.sql
-- Métricas de rendimiento por cohete
-- Autor: Ricardo Edreira
-- Responde: ¿Cuál es el rendimiento de cada cohete?

{{
    config(
        materialized='table'
    )
}}

with launches as (
    select * from {{ ref('stg_launches') }}
    where is_upcoming = false
),

rockets as (
    select * from {{ ref('stg_rockets') }}
),

rocket_stats as (
    select
        r.rocket_id,
        r.rocket_name,
        r.rocket_type,
        r.is_active,
        r.first_flight_date,
        r.cost_per_launch_usd,
        r.height_meters,
        r.mass_kg,
        
        -- Estadísticas de lanzamientos
        count(l.launch_id) as total_missions,
        sum(case when l.is_success = true then 1 else 0 end) as successful_missions,
        sum(case when l.is_success = false then 1 else 0 end) as failed_missions,
        
        -- Tasa de éxito calculada
        round(
            sum(case when l.is_success = true then 1 else 0 end)::decimal / 
            nullif(count(l.launch_id), 0) * 100, 
            2
        ) as calculated_success_rate,
        
        -- Periodo de actividad
        min(l.launch_date) as first_mission_date,
        max(l.launch_date) as last_mission_date,
        
        -- Años activo
        extract(year from max(l.launch_date)) - extract(year from min(l.launch_date)) + 1 as years_in_service,
        
        -- Promedio de misiones por año
        round(
            count(l.launch_id)::decimal / 
            nullif(extract(year from max(l.launch_date)) - extract(year from min(l.launch_date)) + 1, 0),
            2
        ) as avg_missions_per_year
        
    from rockets r
    left join launches l on r.rocket_id = l.rocket_id
    group by 
        r.rocket_id, r.rocket_name, r.rocket_type, r.is_active,
        r.first_flight_date, r.cost_per_launch_usd, r.height_meters, r.mass_kg
)

select 
    *,
    -- Clasificación de confiabilidad
    case 
        when calculated_success_rate >= 95 then 'Excelente'
        when calculated_success_rate >= 80 then 'Bueno'
        when calculated_success_rate >= 60 then 'Regular'
        else 'En desarrollo'
    end as reliability_rating
from rocket_stats
order by total_missions desc
