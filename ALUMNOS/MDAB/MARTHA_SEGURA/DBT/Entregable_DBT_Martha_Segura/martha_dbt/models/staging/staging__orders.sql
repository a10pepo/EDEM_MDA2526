{{ config(
    materialized='view',
    tags=['staging']
) }}

select
    ID         as order_id,
    CUSTOMER   as customer_id,
    ORDERED_AT as ordered_at,
    STORE_ID   as store_id
from {{ source('jaffle_shop', 'orders') }}

