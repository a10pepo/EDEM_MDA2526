
    
    

select
    rocket_id as unique_field,
    count(*) as n_records

from "dev"."main"."stg_rockets"
where rocket_id is not null
group by rocket_id
having count(*) > 1


