{{ config(
    materialized='view',
    tags=['staging']
) }}

select
    id              as order_id,
    customer        as customer_id,
    ordered_at      as ordered_at,
    status          as status
from {{ source('jaffle_shop', 'orders') }}


