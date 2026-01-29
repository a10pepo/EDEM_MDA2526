
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select player_name
from "dev"."main"."top_scorers"
where player_name is null



  
  
      
    ) dbt_internal_test