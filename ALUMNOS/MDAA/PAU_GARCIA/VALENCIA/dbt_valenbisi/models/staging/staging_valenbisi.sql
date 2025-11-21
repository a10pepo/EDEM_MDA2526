with source as (

    select * from {{ source('valenbisi', 'valenbisi_raw') }}

),

renamed as (
    select
        id as id,
        station_id as numero_estacion,
        station_name as nombre_estacion,
        latitude as latitud,
        longitude as longitud,
        available_bikes as bicicletas_disponibles,
        available_slots as huecos_disponibles,
        station_status as estado_estacion,
        total_capacity as capacidad_total,
        cast(timestamp as date) as momento_medicion
    from source
)

select * from renamed