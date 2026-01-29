with source as (
    select * from "dev"."main"."driver_standings"
),

renamed as (
    select
        driver_id,
        cast(season as integer) as season,
        cast(round as integer) as round,
        cast(position as integer) as position,
        cast(points as double) as points,
        cast(wins as integer) as wins
    from source
)

select * from renamed