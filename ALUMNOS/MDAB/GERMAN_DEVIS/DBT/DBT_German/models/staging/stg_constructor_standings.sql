with source as (
    select * from {{ ref('constructor_standings') }}
),

renamed as (
    select
        season as year,
        round,
        constructor_id,
        position,
        points,
        wins
    from source
)

select * from renamed