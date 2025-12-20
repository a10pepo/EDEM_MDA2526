with source as (
    select * from {{ source('f1_raw', 'raw_circuits') }}
),

renamed as (
    select
        circuitId as circuit_id,
        circuitRef as circuit_ref,
        name as nombre_circuito,
        location as localidad,
        country as pais,
        lat as latitud,
        lng as longitud,
        alt as altitud
    from source
)

select * from renamed