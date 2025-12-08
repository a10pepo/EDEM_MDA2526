with source as (

    select * from {{ source('mygoal_raw', 'venues') }}

),

renamed as (
    select
        venueId             as stadium_id,
        fullName            as stadium_name,
        shortName           as stadium_short_name,
        capacity            as capacity,
        city                as city,
        country             as country
    
    from source
)

select * from renamed
