
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select winner
from "dev"."main"."staging_shootouts"
where winner is null



  
  
      
    ) dbt_internal_test