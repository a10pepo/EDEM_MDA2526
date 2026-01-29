
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select match_date
from "dev"."main"."staging_results"
where match_date is null



  
  
      
    ) dbt_internal_test