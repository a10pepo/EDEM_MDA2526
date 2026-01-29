with source as (

    select * from {{ source('mygoal_raw', 'standings') }}

),

renamed as (
    select
        seasonType          as season_type_id,
        year                as season_start_year,
        leagueId            as league_id,
        try_cast(last_matchDateTime as timestamp)   as last_match_at,
        teamRank            as league_position,
        teamId              as team_id,
        gamesPlayed         as matches_played,
        wins                as matches_won,
        ties                as matches_drawn,
        losses              as matches_lost,
        points              as points,
        cast(gf as integer) as goals_for,
        cast(ga as integer) as goals_against,
        gd                  as goals_difference,
        deductions          as points_deduction,
        cast(clean_sheet as integer)                as clean_sheets_count,
        form                as recent_form,
        try_cast(next_opponent as integer)          as next_opponent_team_id,
        next_homeAway       as next_match_side,
        try_cast(next_matchDateTime as timestamp)   as next_match_at,
        timeStamp           as updated_at,
    
    from source
)

select * from renamed
