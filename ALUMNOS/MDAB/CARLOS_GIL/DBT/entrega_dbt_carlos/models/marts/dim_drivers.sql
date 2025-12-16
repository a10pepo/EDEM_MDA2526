-- models/marts/dim_drivers.sql

with drivers as (
    -- Tomamos la información limpia del staging
    select * from {{ ref('stg_drivers') }}
),

driver_standings as (
    -- Usamos la tabla de posiciones para calcular las victorias totales
    select * from {{ ref('stg_driver_standings') }}
),

total_wins as (
    -- Agregamos las victorias totales por piloto
    select
        driver_id,
        sum(wins) as total_career_wins
    from driver_standings
    group by 1
),

final as (
    select
        -- Dimensiones Clave
        t1.driver_id,
        t1.driver_ref,
        t1.forename || ' ' || t1.surname as full_name,
        t1.nationality,
        t1.date_of_birth,
        t1.url,
        
        -- Métrica Calculada
        coalesce(t2.total_career_wins, 0) as total_career_wins
    from drivers as t1
    left join total_wins as t2
        on t1.driver_id = t2.driver_id
)

select * from final