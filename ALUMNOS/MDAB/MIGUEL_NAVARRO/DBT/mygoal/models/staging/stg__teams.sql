with source as (

    select * from {{ source('mygoal_raw', 'teams') }}

),

renamed as (
    select
        teamId              as team_id,     -- 94
        location            as city,    -- Valencia
        name                as team_name,        -- Valencia
        abbreviation        as team_code,        -- VAL
        displayName         as display_name,        -- Valencia
        shortDisplayName    as short_name,        -- Valencia
        color               as primary_color_hex,        -- ffffff
        alternateColor      as secondary_color_hex,        -- 004996
        logoURL             as logo_url,        -- https...
        venueId             as venue_id,
        slug                as team_slug
    
    from source
)

select * from renamed
