{{ config(
    materialized='view',
    tags=['intermediate']
) }}

select
    order_id,
    customer_id,
    store_id,
    {{ generate_date_columns('ordered_at') }},
    count(distinct item_id)        as num_products,
    sum(units)                     as total_units,
    sum(line_subtotal)             as order_subtotal
from {{ ref('intermediate__orders_lineitems') }}
group by
    order_id,
    customer_id,
    store_id,
    date,
    year,
    month,
    day


