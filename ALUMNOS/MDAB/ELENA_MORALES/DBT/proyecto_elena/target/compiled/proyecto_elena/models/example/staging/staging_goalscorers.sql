with source as (
    select * from "dev"."main"."goalscorers"
),
renamed as (
    select
        -- Usamos comillas en "date" para evitar el error de palabra reservada
        cast("date" as date) as match_date,
        
        home_team,
        away_team,
        team,
        scorer,
        minute,
        own_goal, 
        penalty   
    from source
)
select * from renamed