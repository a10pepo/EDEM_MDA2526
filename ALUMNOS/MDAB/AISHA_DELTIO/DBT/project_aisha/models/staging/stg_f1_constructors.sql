with source as (
    select * from {{ source('f1_raw', 'raw_constructors') }}
),

renamed as (
    select
        constructorId as constructor_id,
        constructorRef as constructor_ref,
        name as nombre_escuderia,
        nationality as nacionalidad_escuderia
    from source
)

select * from renamed