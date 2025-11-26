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
        case
            when station_status = 'T' then 'Disponible'
            when station_status = 'F' then 'No disponible'
            else 'Desconocido'
        end as estado_estacion,
        total_capacity as capacidad_total,
        cast(last_update as date) as fecha_medicion,
        cast(last_update as time) as hora_medicion,
        last_update as momento_medicion,   
        timestamp as ultima_consulta
    from source
)

select * from renamed