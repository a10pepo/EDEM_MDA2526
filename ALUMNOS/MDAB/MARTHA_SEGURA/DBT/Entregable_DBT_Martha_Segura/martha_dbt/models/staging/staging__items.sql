{{ config(
    materialized='view',
    tags=['staging']
) }}

select
    id        as item_id,
    order_id,
    sku,
    price,
    Units     as units
from {{ source('jaffle_shop', 'items') }}

