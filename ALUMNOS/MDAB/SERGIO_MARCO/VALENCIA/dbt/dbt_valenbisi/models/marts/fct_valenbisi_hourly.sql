with staging as (
    select * from {{ ref('stg_valenbisi') }}
),

hourly_aggregation as (
    select
        station_id,
        station_name,
        date_trunc('hour', timestamp) as date_hour,
        -- Añadimos las coordenadas aquí
        max(latitude) as latitude,
        max(longitude) as longitude,
        round(avg(available_bikes), 2) as avg_bikes_available,
        round(avg(available_slots), 2) as avg_slots_available,
        max(total_capacity) as total_capacity
    from staging
    group by 1, 2, 3
)

select * from hourly_aggregation