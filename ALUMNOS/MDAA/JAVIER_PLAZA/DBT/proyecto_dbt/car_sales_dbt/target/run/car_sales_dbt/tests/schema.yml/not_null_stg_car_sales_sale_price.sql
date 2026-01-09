
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select sale_price
from "dbt"."main"."stg_car_sales"
where sale_price is null



  
  
      
    ) dbt_internal_test