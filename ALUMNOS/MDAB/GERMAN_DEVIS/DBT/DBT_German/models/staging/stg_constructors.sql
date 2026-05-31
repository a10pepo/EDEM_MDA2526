with source as (
    select * from {{ ref('constructors') }}
),

renamed as (
    select
        constructor_id, -- ESTA LÍNEA DEBE EXISTIR Y ESTAR SIN ERRORES
        name as constructor_name,
        nationality as constructor_nationality
    from source
)

select * from renamed