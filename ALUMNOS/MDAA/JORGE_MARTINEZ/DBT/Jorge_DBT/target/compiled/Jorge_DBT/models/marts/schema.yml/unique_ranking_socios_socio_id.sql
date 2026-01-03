
    
    

select
    socio_id as unique_field,
    count(*) as n_records

from "dev"."main"."ranking_socios"
where socio_id is not null
group by socio_id
having count(*) > 1


