with source as (
    select * from {{ ref('lap_times') }}
),

renamed as (
    select
        raceId as race_id,
        driverId as driver_id,
        lap,
        position,
        time,
        milliseconds
    from source
)

select * from renamed