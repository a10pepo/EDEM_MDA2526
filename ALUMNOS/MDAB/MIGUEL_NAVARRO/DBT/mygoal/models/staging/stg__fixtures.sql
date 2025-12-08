with source as (

    select * from {{ source('mygoal_raw', 'fixtures') }}

),

renamed as (
    select
        Rn                      as source_row_number,
        seasonType              as season_type_id,
        leagueId                as league_id,
        eventId                 as fixture_id,
        date                    as kick_off_time,
        venueId                 as stadium_id,
        attendance              as attendance,
        homeTeamId              as home_team_id,
        awayTeamId              as away_team_id,
        homeTeamWinner          as is_home_winner,
        awayTeamWinner          as is_away_winner,
        homeTeamScore           as home_score,
        awayTeamScore           as away_score,
        homeTeamShootoutScore   as home_penalties_score,
        awayTeamShootoutScore   as away_penalties_score,
        statusId                as status_id,
        updateTime              as updated_at
    
    from source
)

select * from renamed
