with enriched_results as (
    select * from "dev"."main"."int_results_enriched"
),

season_stats as (
    select
        *,
        -- MAGIA 1: Suma acumulativa de puntos por piloto y temporada
        -- Esto permite graficar cómo suben los puntos carrera a carrera
        sum(points) over (
            partition by season, driver_full_name
            order by race_date
            rows between unbounded preceding and current row
        ) as cumulative_points,

        -- MAGIA 2: Conteo acumulativo de victorias
        sum(case when is_winner then 1 else 0 end) over (
            partition by season, driver_full_name
            order by race_date
            rows between unbounded preceding and current row
        ) as cumulative_wins
    from enriched_results
),

championship_standing as (
    select 
        *,
        -- MAGIA 3: ¿En qué posición del campeonato iba el piloto después de esta carrera?
        rank() over (
            partition by season, race_id 
            order by cumulative_points desc, cumulative_wins desc
        ) as championship_position
    from season_stats
)

select 
    race_id,
    season,
    race_name,
    race_date,
    circuit_country,
    driver_full_name,
    driver_nationality,
    constructor_name,
    grid_position,
    finish_position,
    points,
    cumulative_points,
    cumulative_wins,
    championship_position,
    is_winner,
    status
from championship_standing
order by race_date desc, championship_position asc