-- launchpad_stats.sql
-- Estadísticas por plataforma de lanzamiento
-- Autor: Ricardo Edreira
-- Responde: ¿Qué plataforma tiene mejor rendimiento?



with launches as (
    select * from "dev"."main"."stg_launches"
    where is_upcoming = false
),

launchpads as (
    select * from "dev"."main"."stg_launchpads"
),

rockets as (
    select * from "dev"."main"."stg_rockets"
),

pad_stats as (
    select
        lp.launchpad_id,
        lp.launchpad_name,
        lp.launchpad_full_name,
        lp.locality,
        lp.region,
        lp.launchpad_status,
        lp.latitude,
        lp.longitude,
        
        -- Estadísticas de lanzamientos desde nuestros datos
        count(l.launch_id) as launches_in_dataset,
        sum(case when l.is_success = true then 1 else 0 end) as successful_launches,
        sum(case when l.is_success = false then 1 else 0 end) as failed_launches,
        
        -- Tasa de éxito
        round(
            sum(case when l.is_success = true then 1 else 0 end)::decimal / 
            nullif(count(l.launch_id), 0) * 100, 
            2
        ) as success_rate_pct,
        
        -- Periodo de actividad
        min(l.launch_date) as first_launch_date,
        max(l.launch_date) as last_launch_date,
        
        -- Cohetes únicos utilizados
        count(distinct l.rocket_id) as unique_rockets_used,
        
        -- Lista de cohetes (agregación de texto)
        string_agg(distinct r.rocket_name, ', ') as rockets_launched
        
    from launchpads lp
    left join launches l on lp.launchpad_id = l.launchpad_id
    left join rockets r on l.rocket_id = r.rocket_id
    group by 
        lp.launchpad_id, lp.launchpad_name, lp.launchpad_full_name,
        lp.locality, lp.region, lp.launchpad_status, lp.latitude, lp.longitude
)

select 
    *,
    -- Clasificación de actividad
    case 
        when launches_in_dataset >= 50 then 'Alta actividad'
        when launches_in_dataset >= 20 then 'Actividad media'
        when launches_in_dataset > 0 then 'Baja actividad'
        else 'Sin lanzamientos registrados'
    end as activity_level
from pad_stats
order by launches_in_dataset desc