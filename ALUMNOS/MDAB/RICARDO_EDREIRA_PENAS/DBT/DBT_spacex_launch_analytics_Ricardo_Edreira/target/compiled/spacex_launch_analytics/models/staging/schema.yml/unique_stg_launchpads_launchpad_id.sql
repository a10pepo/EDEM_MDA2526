
    
    

select
    launchpad_id as unique_field,
    count(*) as n_records

from "dev"."main"."stg_launchpads"
where launchpad_id is not null
group by launchpad_id
having count(*) > 1


