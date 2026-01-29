
  
  create view "dev"."main"."int_results_enriched__dbt_tmp" as (
    with results as (
    select * from "dev"."main"."stg_results"
),

drivers as (
    select * from "dev"."main"."stg_drivers"
),

constructors as (
    select * from "dev"."main"."stg_constructors"
),

races as (
    select * from "dev"."main"."int_races_circuits" 
)

select
    results.race_id,
    -- Detalles de la carrera (vienen de nuestra tabla intermediate anterior)
    races.season,
    races.race_name,
    races.race_date,
    races.circuit_country,
    
    -- Detalles del piloto
    drivers.first_name || ' ' || drivers.last_name as driver_full_name,
    drivers.driver_nationality,
    
    -- Detalles del equipo
    constructors.constructor_name,
    
    -- Métricas del resultado
    results.grid_position,
    results.position_order as finish_position,
    results.points,
    results.laps,
    results.status,
    
    -- Lógica de negocio simple: ¿Ganó?
    case 
        when results.position_order = 1 then true 
        else false 
    end as is_winner

from results
left join races on results.race_id = races.race_id
left join drivers on results.driver_id = drivers.driver_id
left join constructors on results.constructor_id = constructors.constructor_id
  );
