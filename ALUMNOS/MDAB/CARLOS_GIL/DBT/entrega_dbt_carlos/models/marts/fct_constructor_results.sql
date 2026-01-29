-- models/marts/fct_constructor_results.sql

with constructor_results as (
    -- Tomamos la tabla intermedia que ya une resultados con nombres
    select * from {{ ref('int_constructor_results_enriched') }}
),

races_details as (
    -- Usamos la otra tabla intermedia para obtener el contexto del circuito
    select * from {{ ref('int_races_with_circuits') }}
),

final as (
    select
        -- Claves Primarias y Foráneas (Foreign Keys)
        t1.constructor_results_id,
        t1.race_id,
        t1.constructor_id,
        
        -- Dimensiones Enriquecidas
        t1.constructor_name,
        t1.constructor_nationality,
        t1.race_name,
        t1.race_year,
        t2.country as circuit_country,
        t2.location as circuit_location,
        
        -- Hechos (Métricas)
        t1.points,
        t1.status
    from constructor_results as t1
    left join races_details as t2
        on t1.race_id = t2.race_id
)

select * from final