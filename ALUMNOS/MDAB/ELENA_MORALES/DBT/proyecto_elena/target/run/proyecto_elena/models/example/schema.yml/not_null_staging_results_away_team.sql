
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select away_team
from "dev"."main"."staging_results"
where away_team is null



  
  
      
    ) dbt_internal_test