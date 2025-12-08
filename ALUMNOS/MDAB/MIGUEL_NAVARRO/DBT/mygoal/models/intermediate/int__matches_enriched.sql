{{ config(
    materialized='view'
) }}

with

fixtures as (
    select * from {{ ref('stg__fixtures')}}
),

teams as (
    select * from {{ ref('stg__teams')}}
),

leagues as (
    select * from {{ ref('stg__leagues')}}
),

stadiums as (
    select * from {{ ref('stg__stadiums')}}
)


select

    f.fixture_id,
    f.season_type_id,
    f.league_id,
    
    f.kick_off_time,
    l.league_name,
    l.season_name,
    s.stadium_name,
    s.city as match_city,

    f.home_team_id,
    home.team_name as home_team_name,
    home.team_code as home_team_code,
    f.home_score,
    
    f.away_team_id,
    away.team_name as away_team_name,
    away.team_code as away_team_code,
    f.away_score,

    case
        when f.home_score > f.away_score then 'Home Win'
        when f.away_score > f.home_score then 'Away Win'
        else 'Draw'
    end as match_result,

    case
        when f.home_score > f.away_score then f.home_team_id
        when f.away_score > f.home_score then f.away_team_id
        else null
    end as winner_team_id

from fixtures f

left join 
    teams home on f.home_team_id = home.team_id

left join
    teams away on f.away_team_id = away.team_id

left join
    leagues l on f.league_id = l.league_id and f.season_type_id = l.season_type_id

left join
    stadiums s on f.stadium_id = s.stadium_id

