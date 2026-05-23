
    
    

select
    id as unique_field,
    count(*) as n_records

from "dev"."main"."raw_rockets"
where id is not null
group by id
having count(*) > 1


