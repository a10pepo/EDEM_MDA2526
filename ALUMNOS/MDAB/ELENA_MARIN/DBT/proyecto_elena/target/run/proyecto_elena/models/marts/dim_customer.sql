
  
    
    

    create  table
      "dev"."main"."dim_customer__dbt_tmp"
  
    as (
      select
    customer_id,
    first_name,
    last_name,
    customer_name,
    email,
    telephone,
    city,
    country,
    gender,
    job_title,
    date_of_birth,
    age
from "dev"."main"."int_customers_clean"
    );
  
  