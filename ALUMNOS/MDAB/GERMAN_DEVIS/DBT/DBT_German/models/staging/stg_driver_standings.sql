with source as (
    select * from {{ ref('driver_standings') }}
),

renamed as (
    select
        season as year,
        round,
        driver_id,
        position,
        points,
        wins
    from source
)

select * from renamed