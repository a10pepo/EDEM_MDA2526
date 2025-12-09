with products as (

    select * from {{ ref('staging__products') }}

),


products_orders as (

    select
        product_id,
        count(distinct order_id)      as total_orders,
        min(order_date)               as first_order_date,
        max(order_date)               as last_order_date,

        sum(case when order_date >= date_add(-365, current_date) then original_quantity else 0 end)        as original_quantity_sold_in_last_365_days,
        sum(case when order_date >= date_add(-365, current_date) then final_quantity else 0 end)           as final_quantity_sold_in_last_365_days,
        sum(case when order_date >= date_add(-365, current_date) then original_subtotal_price else 0 end)  as original_subtotal_price_in_last_365_days,
        sum(case when order_date >= date_add(-365, current_date) then final_subtotal_price else 0 end)     as final_subtotal_price_in_last_365_days,

        sum(case when order_date >= date_add(-180, current_date) then original_quantity else 0 end)        as original_quantity_sold_in_last_180_days,
        sum(case when order_date >= date_add(-180, current_date) then final_quantity else 0 end)           as final_quantity_sold_in_last_180_days,
        sum(case when order_date >= date_add(-180, current_date) then original_subtotal_price else 0 end)  as original_subtotal_price_in_last_180_days,
        sum(case when order_date >= date_add(-180, current_date) then final_subtotal_price else 0 end)     as final_subtotal_price_in_last_180_days
    from 
        {{ ref('marts__order_lineitems') }}
    group by 
        product_id
)

 select
    products.*, 
    coalesce(total_orders, 0) as total_orders,
    first_order_date,
    last_order_date,

    coalesce(original_quantity_sold_in_last_365_days, 0)  as original_quantity_sold_in_last_365_days,
    coalesce(final_quantity_sold_in_last_365_days, 0)     as final_quantity_sold_in_last_365_days,
    coalesce(original_subtotal_price_in_last_365_days, 0) as original_subtotal_price_in_last_365_days,
    coalesce(final_subtotal_price_in_last_365_days, 0)    as final_subtotal_price_in_last_365_days,

    coalesce(original_quantity_sold_in_last_180_days, 0)  as original_quantity_sold_in_last_180_days,
    coalesce(final_quantity_sold_in_last_180_days, 0)     as final_quantity_sold_in_last_180_days,
    coalesce(original_subtotal_price_in_last_180_days, 0) as original_subtotal_price_in_last_180_days,
    coalesce(final_subtotal_price_in_last_180_days, 0)    as final_subtotal_price_in_last_180_days
 from 
    products
left join 
    products_orders 
on products.product_id = products_orders.product_id
