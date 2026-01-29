with pit_stops as (
    select * from {{ ref('stg_pit_stops') }}
),

aggregated as (
    select
        race_id,
        driver_id,
        count(stop) as total_pit_stops,
        -- Sumamos milisegundos para tener el tiempo total en boxes
        sum(milliseconds) as total_time_in_pits_ms,
        max(duration) as longest_pit_stop_duration
    from pit_stops
    group by 1, 2
)

select * from aggregated