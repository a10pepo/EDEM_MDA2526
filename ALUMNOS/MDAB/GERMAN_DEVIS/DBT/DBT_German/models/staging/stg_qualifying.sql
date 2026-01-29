with source as (
    select * from {{ ref('qualifying') }}
),

renamed as (
    select
        -- Clave compuesta artificial (carrera + piloto)
        race_id || '-' || driver_id as qualifying_id,
        race_id,
        driver_id,
        constructor_id,
        position as qualifying_position,
        q1 as q1_time,
        q2 as q2_time,
        q3 as q3_time
    from source
)

select * from renamed