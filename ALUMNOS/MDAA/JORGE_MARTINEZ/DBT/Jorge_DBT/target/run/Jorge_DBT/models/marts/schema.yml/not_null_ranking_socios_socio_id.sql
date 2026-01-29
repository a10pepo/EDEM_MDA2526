
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select socio_id
from "dev"."main"."ranking_socios"
where socio_id is null



  
  
      
    ) dbt_internal_test