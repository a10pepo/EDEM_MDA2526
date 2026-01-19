
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select launch_id
from "dev"."main"."stg_launches"
where launch_id is null



  
  
      
    ) dbt_internal_test