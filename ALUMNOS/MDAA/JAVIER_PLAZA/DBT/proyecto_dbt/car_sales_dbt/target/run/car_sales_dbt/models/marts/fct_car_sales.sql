
  
    
    

    create  table
      "dbt"."main"."fct_car_sales__dbt_tmp"
  
    as (
      with base as (
    select * from "dbt"."main"."stg_car_sales"
),
dim as (
    select * from "dbt"."main"."dim_salespersons"
),
joined as (
    select
        md5(concat(sale_date,customer_name,car_model,sale_price)) as sale_id,
        dim.salesperson_id,
        base.*
    from base
    left join dim 
        on dim.salesperson_name = base.salesperson
)

select * from joined
    );
  
  