{{ config(
    materialized='table',
    tags=['marts', 'clientes']
) }}

select
    customer_id,
    count(distinct order_id)    as num_pedidos,
    min(ordered_at)             as first_order_at,
    max(ordered_at)             as last_order_at,
    sum(order_subtotal)         as lifetime_revenue
from {{ ref('intermediate__orders') }}
group by customer_id
--Algo tipo “clientes activos en el último mes”, “cuántas compras ha hecho cada cliente…”