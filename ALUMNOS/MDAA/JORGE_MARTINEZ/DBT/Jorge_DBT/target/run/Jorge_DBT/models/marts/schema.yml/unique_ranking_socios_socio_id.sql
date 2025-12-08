
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    socio_id as unique_field,
    count(*) as n_records

from "dev"."main"."ranking_socios"
where socio_id is not null
group by socio_id
having count(*) > 1



  
  
      
    ) dbt_internal_test