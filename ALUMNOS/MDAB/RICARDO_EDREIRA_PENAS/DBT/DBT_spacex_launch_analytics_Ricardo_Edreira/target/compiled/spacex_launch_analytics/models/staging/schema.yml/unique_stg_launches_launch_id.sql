
    
    

select
    launch_id as unique_field,
    count(*) as n_records

from "dev"."main"."stg_launches"
where launch_id is not null
group by launch_id
having count(*) > 1


