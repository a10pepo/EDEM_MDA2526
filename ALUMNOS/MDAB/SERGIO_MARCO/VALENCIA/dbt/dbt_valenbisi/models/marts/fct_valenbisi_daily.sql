with staging as (
    select * from {{ ref('stg_valenbisi') }}
),

daily_aggregation as (
    select
        station_id,
        station_name,
        date_trunc('day', timestamp) as date_day,
        -- Añadimos las coordenadas aquí
        max(latitude) as latitude,
        max(longitude) as longitude,
        round(avg(available_bikes), 2) as avg_bikes_available,
        round(avg(available_slots), 2) as avg_slots_available,
        max(total_capacity) as total_capacity
    from staging
    group by 1, 2, 3
)

select * from daily_aggregation