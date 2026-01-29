with base as (
    select distinct salesperson 
    from {{ ref('stg_car_sales') }}
)

select
    salesperson as salesperson_name,
    md5(salesperson) as salesperson_id
from base
