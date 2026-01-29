{{ config(
    materialized='view',
    tags=['staging']
) }}

select
    ID   as customer_id,
    NAME as customer_name
from {{ source('jaffle_shop', 'customers') }}

