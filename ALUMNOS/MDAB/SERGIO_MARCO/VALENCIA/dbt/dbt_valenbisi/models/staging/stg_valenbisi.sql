with source as (
    -- Referencia a la tabla cruda cargada por tu script de Python
    select * from {{ source('public', 'valenbisi_raw') }}
),

renamed as (
    select
        -- Identificadores y nombres
        station_id,
        station_name,
        
        -- Coordenadas
        latitude,
        longitude,
        
        -- Métricas de disponibilidad (sin traducir)
        available_bikes,
        available_slots,
        total_capacity,
        
        -- Transformación lógica a booleano (mantenemos el nombre de la columna)
        case 
            when station_status = 'T' then true 
            else false 
        end as station_status,

        -- Referencia temporal
        timestamp

    from source
)

select * from renamed