{{ config(
    materialized='view',
    tags=['intermediate']
) }}

with orders as (
    select * from {{ ref('staging__orders') }}
),

items as (
    select * from {{ ref('staging__items') }}
)

select
    o.order_id,
    o.customer_id,
    o.ordered_at,
    o.store_id,
    i.item_id,
    i.sku,
    i.units,
    i.price,
    i.units * i.price as line_subtotal
from orders o
join items i
    on o.order_id = i.order_id

