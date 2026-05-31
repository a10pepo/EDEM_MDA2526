-- launches_summary.sql
-- Resumen de lanzamientos por año y cohete
-- Autor: Ricardo Edreira
-- Responde: ¿Cómo ha evolucionado la actividad de lanzamiento por año?



with launches as (
    select * from "dev"."main"."stg_launches"
    where is_upcoming = false
),

rockets as (
    select * from "dev"."main"."stg_rockets"
),

summary as (
    select
        l.launch_year,
        r.rocket_name,
        
        -- Conteos
        count(*) as total_launches,
        sum(case when l.is_success = true then 1 else 0 end) as successful_launches,
        sum(case when l.is_success = false then 1 else 0 end) as failed_launches,
        sum(case when l.is_success is null then 1 else 0 end) as unknown_outcome,
        
        -- Tasa de éxito
        round(
            sum(case when l.is_success = true then 1 else 0 end)::decimal / 
            nullif(count(*), 0) * 100, 
            2
        ) as success_rate_pct,
        
        -- Primer y último lanzamiento del año
        min(l.launch_date) as first_launch_of_year,
        max(l.launch_date) as last_launch_of_year
        
    from launches l
    left join rockets r on l.rocket_id = r.rocket_id
    where l.launch_year is not null
    group by l.launch_year, r.rocket_name
)

select 
    *,
    -- Ranking por volumen de lanzamientos
    row_number() over (partition by launch_year order by total_launches desc) as rocket_rank_by_year
from summary
order by launch_year desc, total_launches desc