with customers as (

    select * from {{ ref('staging__customers') }}

),

orders as (

    select * from {{ ref('marts__orders') }}

),

customer_orders_summary as (

    select
        customer_id,
        count(distinct order_id)     as lifetime_num_orders,
        count(distinct order_id) > 1 as is_repeat_buyer,
        min(order_date)              as first_order_date,
        max(order_date)              as last_order_date,
        sum(final_total_price)       as lifetime_value
    from orders
    group by 1

),

joined as (

    select
        customers.*,
        coalesce(lifetime_num_orders, 0) as lifetime_num_orders,
        coalesce(is_repeat_buyer, False) as is_repeat_buyer,
        first_order_date,
        last_order_date,
        coalesce(lifetime_value, 0) as lifetime_value
    from    
        customers
    left join 
        customer_orders_summary
    on 
        customers.customer_id = customer_orders_summary.customer_id

)

select * from joined
