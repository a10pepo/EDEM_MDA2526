with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

final as (
    select
        -- IDs clave
        order_items.order_item_id,
        orders.order_id,
        orders.user_id,
        products.product_id,

        -- Dimensiones (para filtrar)
        orders.order_date,
        orders.order_status,
        products.category as product_category,
        products.brand as product_brand,
        products.product_name,

        -- Métricas (para sumar)
        order_items.quantity,
        order_items.item_price,
        order_items.item_total,
        
        -- Cálculo útil: ¿Cuánto costó vs cuánto se vendió? (Si tuviéramos coste)
        -- Por ahora calculamos el peso del ítem en el pedido total
        (order_items.item_total / nullif(orders.total_amount, 0)) as pct_of_order_total

    from order_items
    left join orders on order_items.order_id = orders.order_id
    left join products on order_items.product_id = products.product_id
)

select * from final