with constructor_results as (
    select * from {{ ref('stg_constructor_results') }} -- Asegúrate de usar el nombre que le dimos al modelo staging
),

constructors as (
    select * from {{ ref('stg_constructors') }}
),

races as (
    select * from {{ ref('stg_races') }}
),

joined as (
    select
        -- IDs
        res.constructor_results_id,
        res.race_id,
        res.constructor_id,
        
        -- Dimensiones (Nombres)
        cons.name as constructor_name,
        cons.nationality as constructor_nationality,
        races.year as race_year,
        races.name as race_name,
        
        -- Métricas
        res.points,
        res.status
    from constructor_results as res
    left join constructors as cons
        on res.constructor_id = cons.constructor_id
    left join races
        on res.race_id = races.race_id
)

select * from joined