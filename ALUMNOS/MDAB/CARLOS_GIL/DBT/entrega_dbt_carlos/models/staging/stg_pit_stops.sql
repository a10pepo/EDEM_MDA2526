with source as (
    select * from {{ ref('pit_stops') }}
),

renamed as (
    select
        raceId as race_id,
        driverId as driver_id,
        stop,
        lap,
        time,
        duration,
        milliseconds
    from source
)

select * from renamed