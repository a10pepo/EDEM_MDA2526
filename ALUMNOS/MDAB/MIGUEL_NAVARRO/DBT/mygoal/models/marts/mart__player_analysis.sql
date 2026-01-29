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
    squads.team_id          as team_id,
    squads.player_id        as player_id,
    squads.season_year      as season_year,

    squads.position_name    as position_name,
    squads.jersey_number    as jersey,
    players.player_name     as player_name,

    players.nationality     as nationality,
    players.gender          as gender,

    teams.team_name         as team_name,
    teams.team_code         as team_code,
    teams.city              as team_city,

    players.height_cm       as height_cm,
    players.weight_kg       as weight_kg,

    players.birth_date      as birth_date,
    date_diff('year', players.birth_date, current_date) as current_age,

from
    squads

left join
    players 
    on squads.player_id = players.player_id

left join
    teams
    on squads.team_id = teams.team_id

