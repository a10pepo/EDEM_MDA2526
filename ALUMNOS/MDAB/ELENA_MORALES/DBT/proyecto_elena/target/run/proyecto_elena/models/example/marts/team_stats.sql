
  
  create view "dev"."main"."team_stats__dbt_tmp" as (
    with matches as (
    select * from "dev"."main"."staging_results"
),

-- 1. Calculate stats when playing as HOME team
home_stats as (
    select
        home_team as team,
        count(*) as games_played,
        -- Win logic: Home Score > Away Score
        sum(case when home_score > away_score then 1 else 0 end) as wins,
        sum(home_score) as goals_for
    from matches
    group by 1
),

-- 2. Calculate stats when playing as AWAY team
away_stats as (
    select
        away_team as team,
        count(*) as games_played,
        -- Win logic: Away Score > Home Score
        sum(case when away_score > home_score then 1 else 0 end) as wins,
        sum(away_score) as goals_for
    from matches
    group by 1
),

-- 3. Join both sides to get total stats
final_stats as (
    select
        coalesce(h.team, a.team) as team,
        (coalesce(h.games_played, 0) + coalesce(a.games_played, 0)) as total_games,
        (coalesce(h.wins, 0) + coalesce(a.wins, 0)) as total_wins,
        (coalesce(h.goals_for, 0) + coalesce(a.goals_for, 0)) as total_goals
    from home_stats h
    full outer join away_stats a on h.team = a.team
)

select * from final_stats
order by total_wins desc
  );
