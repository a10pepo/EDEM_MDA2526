
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select launchpad_id
from "dev"."main"."launchpad_stats"
where launchpad_id is null



  
  
      
    ) dbt_internal_test