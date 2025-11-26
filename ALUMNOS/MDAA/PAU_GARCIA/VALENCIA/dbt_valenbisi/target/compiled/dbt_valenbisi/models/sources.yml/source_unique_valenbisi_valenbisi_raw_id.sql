
    
    

select
    id as unique_field,
    count(*) as n_records

from "valenbisi_db"."public"."valenbisi_raw"
where id is not null
group by id
having count(*) > 1


