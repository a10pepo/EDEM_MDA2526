with source as (
    select * from "dev"."main"."raw_socios"
),
renamed as (
    select
        id as socio_id,
        nombre,
        equipo_favorito,
        nivel_socio
    from source
)
select * from renamed