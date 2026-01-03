
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select team
from "dev"."main"."team_stats"
where team is null



  
  
      
    ) dbt_internal_test