
  
    
    

    create  table
      "dbt"."main"."dim_salespersons__dbt_tmp"
  
    as (
      with base as (
    select distinct salesperson 
    from "dbt"."main"."stg_car_sales"
)

select
    salesperson as salesperson_name,
    md5(salesperson) as salesperson_id
from base
    );
  
  