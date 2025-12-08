with source as (

    select * from {{ source('mygoal_raw', 'players') }}

),

renamed as (
    select
        athleteId               as player_id,
        firstName               as first_name,
        middleName              as middle_name,
        lastName                as last_name,
        fullName                as full_name,
        displayName             as player_name,
        shortName               as short_name,
        nickName                as nickname,
        slug                    as player_slug,
        {{ lbs_to_kg('weight') }}       as weight_kg,
        {{ inches_to_cm('height') }}    as height_cm,
        try_cast(left(dateOfBirth, 10) as date)     as birth_date,
        gender                  as gender,
        cast(jersey as integer) as jersey_current_number,
        citizenship             as nationality,
        birthPlaceCountry       as birth_country,
        positionName            as position_name,
        positionAbbreviation    as position_code,
        headshotUrl             as player_image_url,
        timestamp               as updated_at
    
    from source
)

select * from renamed
