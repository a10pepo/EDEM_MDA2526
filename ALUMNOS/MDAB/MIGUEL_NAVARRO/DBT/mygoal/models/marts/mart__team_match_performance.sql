{{ config(
    materialized='table'
) }}

with

st as (
    select * from {{ ref('stg__team_stats')}}
),

ma as (
    select * from {{ ref('int__matches_enriched')}}
)


select

    st.team_id              as team_id,
    st.fixture_id           as fixture_id,
    st.season_type_id       as season_type_id,

    ma.kick_off_time        as kick_off,
    ma.league_name          as league_name,
    ma.season_name          as season_name,

    case
        when st.team_id = ma.home_team_id then ma.home_team_name
        when st.team_id = ma.away_team_id then ma.away_team_name
    end as team_name,

    st.team_side            as team_side,

    case
        when ma.winner_team_id = st.team_id then 'Win'
        when ma.match_result = 'Draw' then 'Draw'
        else 'Loss'
    end as match_outcome,

    st.possession_percentage    as possession_percentage,
    st.shot_accuracy            as shot_accuracy,
    st.shots_total              as shots_total,
    st.shots_on_target          as shots_on_target,
    st.pass_accuracy            as pass_accuracy,
    st.tackles_total            as tackles_total,
    st.tackles_won              as tackles_won,
    st.fouls_committed          as fouls_committed,
    st.yellow_cards             as yellow_cards,
    st.red_cards                as red_cards

from
    stg__team_stats st

left join
    int__matches_enriched ma
    on st.fixture_id = ma.fixture_id
