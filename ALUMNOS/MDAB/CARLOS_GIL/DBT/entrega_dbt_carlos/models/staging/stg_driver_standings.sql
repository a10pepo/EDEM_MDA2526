with source as (
    select * from {{ ref('driver_standings') }}
),

renamed as (
    select
        driverStandingsId as driver_standings_id,
        raceId as race_id,
        driverId as driver_id,
        points,
        position,
        positionText as position_text,
        wins
    from source
)

select * from renamed