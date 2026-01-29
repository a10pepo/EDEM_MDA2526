{{ config(
    materialized='table'
) }}

with users as (
    select * from {{ ref('stg_users') }}
),

-- 1. Métricas de Ventas (LTV, número de pedidos)
user_orders as (
    select
        user_id,
        count(distinct order_id) as total_orders,
        sum(total_amount) as lifetime_value,
        min(order_date) as first_order_date,
        max(order_date) as last_order_date
    from {{ ref('stg_orders') }}
    group by user_id
),

-- 2. Métricas de Comportamiento (Eventos en la web)
user_events as (
    select
        user_id,
        max(event_timestamp) as last_seen_at,
        count(event_id) as total_web_events,
        -- Contamos cuántas veces añadió al carrito
        sum(case when event_type = 'cart' then 1 else 0 end) as total_add_to_carts
    from {{ ref('stg_events') }}
    group by user_id
),

-- 3. Métricas de Feedback (Reviews)
user_reviews as (
    select
        user_id,
        count(review_id) as total_reviews_written,
        avg(rating) as avg_rating_given
    from {{ ref('stg_reviews') }}
    group by user_id
),

final as (
    select
        u.user_id,
        u.name,
        u.email,
        u.city,
        u.signup_date,

        -- Métricas calculadas (coalesce pone un 0 si es null)
        coalesce(uo.total_orders, 0) as total_orders,
        coalesce(uo.lifetime_value, 0) as lifetime_value,
        uo.last_order_date,
        
        coalesce(ue.total_web_events, 0) as total_web_events,
        coalesce(ue.total_add_to_carts, 0) as total_add_to_carts,
        ue.last_seen_at,

        coalesce(ur.total_reviews_written, 0) as total_reviews_written

    from users u
    left join user_orders uo on u.user_id = uo.user_id
    left join user_events ue on u.user_id = ue.user_id
    left join user_reviews ur on u.user_id = ur.user_id
)

select * from final