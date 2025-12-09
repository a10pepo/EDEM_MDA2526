with order_lineitems as (

    select * from {{ ref('intermediate__order_lineitems') }}

),

locations as (

    select * from {{ ref('staging__locations') }}
),

customers as (

    select * from {{ ref('staging__customers') }}
),

products as (

    select * from {{ ref('staging__products') }}
)

 select
    order_date,
    locations.location_id,
    locations.location_name,
    customers.customer_id,
    customers.customer_name,
    order_id,
    products.product_id,
    products.product_name,
    products.product_type,
    original_quantity,
    final_quantity,
    unit_price,
    original_subtotal_price,
    final_subtotal_price,
    (1 + tax_rate) * original_subtotal_price as original_total_price,
    (1 + tax_rate) * final_subtotal_price    as final_total_price,
    has_returned_items
 from 
    order_lineitems
left join 
    locations 
on order_lineitems.location_id = locations.location_id
left join
    customers
on order_lineitems.customer_id = customers.customer_id
left join 
    products
on order_lineitems.product_id = products.product_id