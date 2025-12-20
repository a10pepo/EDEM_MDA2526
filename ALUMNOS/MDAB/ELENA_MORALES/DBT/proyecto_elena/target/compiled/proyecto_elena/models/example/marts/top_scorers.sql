-- Este modelo responde a la pregunta: 
-- "¿Quiénes son los máximos goleadores de la historia y cuántos penaltis han marcado?".

with goals as (
    select * from "dev"."main"."staging_goalscorers"
)

select
    scorer as player_name,
    team as national_team,
    count(*) as total_goals,
    sum(case when penalty = TRUE then 1 else 0 end) as penalty_goals
from goals
-- Exclude own goals (goals scored against themselves)
where own_goal = FALSE
group by 1, 2
order by total_goals desc