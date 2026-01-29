
    
    

select
    salesperson_id as unique_field,
    count(*) as n_records

from "dbt"."main"."dim_salespersons"
where salesperson_id is not null
group by salesperson_id
having count(*) > 1


