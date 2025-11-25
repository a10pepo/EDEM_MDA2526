
  create view "valenbisi_db"."public"."staging_valenbisi__dbt_tmp"
    
    
  as (
    with source as (

    select * from "valenbisi_db"."public"."valenbisi_raw"

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
        cast(timestamp as date) as momento_medicion
    from source
)

select * from renamed
  );