with source as (
    select * from {{ source('f1_raw', 'raw_races') }}
),

renamed as (
    select
        raceId as race_id,
        year as temporada,
        round as ronda,
        circuitId as circuit_id,
        name as nombre_gran_premio,
        try_cast(date as date) as fecha_carrera,
        try_cast(time as time) as hora_carrera,
        -- Creamos un timestamp completo para análisis precisos de tiempo
        try_cast(date || ' ' || coalesce(time, '00:00:00') as timestamp) as momento_carrera
    from source
)

select * from renamed