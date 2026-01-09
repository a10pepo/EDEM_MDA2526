{{ config(
    materialized='table'
) }}

with int_orders as (
    select * from {{ ref('int_order') }}
)

select
    order_item_id,
    order_id,
    user_id,
    product_id,
    order_date,
    product_category,
    product_brand,
    quantity,
    item_price,
    item_total
from int_orders
-- Aquí podrías filtrar pedidos cancelados si quisieras
-- where order_status != 'cancelled'