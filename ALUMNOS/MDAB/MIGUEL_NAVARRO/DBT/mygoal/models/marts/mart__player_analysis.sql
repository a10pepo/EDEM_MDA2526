{{ config(
    materialized='table'
) }}

with

squads as (
    select * from {{ ref('stg__squads')}}
),

players as (
    select * from {{ ref('stg__players')}}
),

teams as (
    select * from {{ ref('stg__teams')}}
)

select
    squads.team_id,
    squads.player_id,
    squads.season_year,

    squads.position_name,
    squads.jersey_number,
    players.player_name,

    players.nationality,
    players.gender,

    teams.team_name,
    teams.team_code,
    teams.city as team_city,

    players.height_cm,
    players.weight_kg,

    players.birth_date,
    date_diff('year', players.birth_date, current_date) as current_age,

from
    squads

left join
    players 
    on squads.player_id = players.player_id

left join
    teams
    on squads.team_id = teams.team_id

