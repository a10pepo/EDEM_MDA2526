{{ config(materialized='view') }}

with capturas as (
    select * from {{ ref('staging__capturas') }}
)

select
    articulo_id,
    
    -- Agregaciones
    count(captura_id) as total_capturas_registradas,
    avg(peso_kg) as peso_medio_kg,
    max(peso_kg) as record_peso_kg,
    min(peso_kg) as peso_minimo_kg,
    
    -- Especies más comunes (Truco: string_agg en duckdb concatena textos)
    -- Esto nos dará una lista separada por comas de qué se pesca con esto
    string_agg(distinct especie, ', ') as especies_objetivo

from capturas
group by articulo_id