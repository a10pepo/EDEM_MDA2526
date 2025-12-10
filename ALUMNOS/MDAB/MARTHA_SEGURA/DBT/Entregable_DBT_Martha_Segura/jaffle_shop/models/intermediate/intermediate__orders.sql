with order_lineitems as (

    select * from {{ ref('staging__order_lineitems') }}

),

orders as (

    select * from {{ ref('staging__orders') }}

)



-- Este modelo tiene mucha complejidad. ¿La podriamos reducir?
select
    orders.order_date,
    orders.location_id,
    orders.customer_id,
    order_lineitems.order_id,
    count(distinct order_lineitems.product_id) as numper_of_products,
    sum(case when type_of_movement = 'VENTA' then order_lineitems.quantity else 0 end)       as original_quantity,
    sum(order_lineitems.quantity)                                                            as final_quantity,
    sum(case when type_of_movement = 'VENTA' then order_lineitems.subtotal_price else 0 end) as original_subtotal_price,
    sum(order_lineitems.subtotal_price)                                                      as final_subtotal_price,
    max(type_of_movement == 'DEVOLUCION')                                                    as has_returned_items      
from 
    order_lineitems 
inner join 
    orders  
on order_lineitems.order_id = orders.order_id
group by 
    orders.order_date,
    orders.location_id,
    orders.customer_id,
    order_lineitems.order_id,
