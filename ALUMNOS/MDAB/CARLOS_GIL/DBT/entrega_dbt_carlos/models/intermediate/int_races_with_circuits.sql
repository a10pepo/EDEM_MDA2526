with races as (
    select * from {{ ref('stg_races') }}
),

circuits as (
    select * from {{ ref('stg_circuits') }}
),

joined as (
    select
        races.race_id,
        races.year,
        races.round,
        races.name as race_name,
        races.date as race_date,
        -- Información del circuito enriquecida
        circuits.circuit_id,
        circuits.location,
        circuits.country,
        circuits.latitude,
        circuits.longitude
    from races
    left join circuits
        on races.circuit_id = circuits.circuit_id
)

select * from joined