with source as (
    select * from {{ ref('constructor_standings') }}
),

renamed as (
    select
        constructorStandingsId as constructor_standings_id,
        raceId as race_id,
        constructorId as constructor_id,
        points,
        position,
        positionText as position_text,
        wins
    from source
)

select * from renamed