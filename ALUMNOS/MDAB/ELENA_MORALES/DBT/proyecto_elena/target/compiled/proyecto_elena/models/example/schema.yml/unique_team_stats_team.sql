
    
    

select
    team as unique_field,
    count(*) as n_records

from "dev"."main"."team_stats"
where team is not null
group by team
having count(*) > 1


