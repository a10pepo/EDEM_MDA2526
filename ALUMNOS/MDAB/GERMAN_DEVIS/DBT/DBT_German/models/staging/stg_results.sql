with source as (
    select * from {{ ref('results') }}
),

renamed as (
    select
        -- Generamos una clave primaria artificial porque tu tabla no tiene 'result_id'
        -- Usamos la combinación de carrera y piloto que es única
        race_id || '-' || driver_id as result_id, 
        race_id,
        driver_id,
        constructor_id,
        grid as grid_position,
        position as finish_position,
        position_order,
        points,
        laps,
        status
        -- No tienes columnas de tiempo ni vuelta rápida, así que no las ponemos
    from source
)

select * from renamed