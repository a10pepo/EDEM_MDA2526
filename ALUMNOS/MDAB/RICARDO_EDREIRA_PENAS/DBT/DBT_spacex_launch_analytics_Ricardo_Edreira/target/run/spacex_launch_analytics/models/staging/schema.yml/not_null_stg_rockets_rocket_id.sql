
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select rocket_id
from "dev"."main"."stg_rockets"
where rocket_id is null



  
  
      
    ) dbt_internal_test