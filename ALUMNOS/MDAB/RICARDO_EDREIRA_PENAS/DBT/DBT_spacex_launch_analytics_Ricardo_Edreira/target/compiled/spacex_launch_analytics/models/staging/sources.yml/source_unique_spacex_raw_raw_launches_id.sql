
    
    

select
    id as unique_field,
    count(*) as n_records

from "dev"."main"."raw_launches"
where id is not null
group by id
having count(*) > 1


