{{ config(
    materialized='table',
    tags=['marts', 'ventas']
) }}

select
    sku,
    sum(units)         as unidades_vendidas,
    sum(line_subtotal) as total_ventas
from {{ ref('intermediate__orders_lineitems') }}
group by sku

--Responde a “total de ventas por producto” y “top 10 productos”