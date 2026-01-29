with source as (

    select * from {{ source('mygoal_raw', 'teamRoster') }}

),

renamed as (
    select
        seasonYear              as season_year,
        seasonType              as season_type_id,
        teamId                  as team_id,
        teamName                as team_name,
        athleteId               as player_id,
        playerDisplayName       as player_name,
        cast(jersey as integer) as jersey_number,
        position                as position_name,
        timeStamp               as updated_at
    
    from source
)

select * from renamed
