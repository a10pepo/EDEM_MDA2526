
  
  create view "dev"."main"."int_races_circuits__dbt_tmp" as (
    with races as (
    select * from "dev"."main"."stg_races"
),

circuits as (
    select * from "dev"."main"."stg_circuits"
)

select
    races.race_id,
    races.season,
    races.round,
    races.race_name,
    races.race_date,
    races.race_time,
    -- Información del circuito unida
    circuits.circuit_name,
    circuits.city as circuit_city,
    circuits.country as circuit_country,
    circuits.latitude,
    circuits.longitude
from races
left join circuits 
    on races.circuit_id = circuits.circuit_id
  );
