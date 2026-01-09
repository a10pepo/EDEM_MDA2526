
  
    
    

    create  table
      "dev"."main"."fct_store_product_prices__dbt_tmp"
  
    as (
      select
    store_id,
    store_name,
    store_country,
    store_city,
    product_id,
    category,
    sub_category,
    production_cost,
    suggested_price,
    local_price,
    price_effective_date
from "dev"."main"."int_store_products"
    );
  
  