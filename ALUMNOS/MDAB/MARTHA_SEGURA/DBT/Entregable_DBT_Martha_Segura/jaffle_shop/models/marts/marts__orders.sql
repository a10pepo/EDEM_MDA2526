with order_lineitems as (

    select * from {{ ref('marts__order_lineitems') }}

)


select
    order_date,
    location_id,
    location_name,
    customer_id,
    customer_name,
    order_id,
    count(distinct product_id)     as number_of_products,
    max(product_type = 'jaffle')   as has_food_products,
    max(product_type = 'beverage') as has_drink_products,
    sum(original_quantity)         as original_quantity,
    sum(final_quantity)            as final_quantity,
    sum(original_subtotal_price)   as original_subtotal_price,
    sum(final_subtotal_price)      as final_subtotal_price,
    sum(original_total_price)      as original_total_price,
    sum(final_total_price)         as final_total_price,
    max(has_returned_items)        as has_returned_items
 from 
    order_lineitems
group by 
    order_date,
    location_id,
    location_name,
    customer_id,
    customer_name,
    order_id