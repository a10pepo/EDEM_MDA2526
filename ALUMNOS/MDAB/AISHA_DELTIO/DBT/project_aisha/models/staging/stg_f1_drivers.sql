with source as (
    select * from {{ source('f1_raw', 'raw_drivers') }}
),

renamed as (
    select
        driverId as driver_id,
        driverRef as driver_ref,
        number as numero_permanente,
        code as codigo_piloto,
        -- Concatenamos nombre y apellido para no tenerlo separado siempre
        forename || ' ' || surname as nombre_completo,
        -- Convertimos texto a fecha real
        try_cast(dob as date) as fecha_nacimiento,
        nationality as nacionalidad,
        url as url_wiki
    from source
)

select * from renamed