with source as (
    select * from {{ ref('races') }}
),

renamed as (
    select
        raceId as race_id,
        year,
        round,
        circuitId as circuit_id,
        name,
        date,
        time,
        url
        -- He omitido las columnas de free practice (fp1, fp2...) por limpieza,
        -- pero puedes añadirlas si las necesitas.
    from source
)

select * from renamed