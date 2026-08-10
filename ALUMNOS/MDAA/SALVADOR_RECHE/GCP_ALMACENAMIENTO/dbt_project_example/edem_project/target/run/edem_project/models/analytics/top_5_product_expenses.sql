
  
    

    create or replace table `e2e-gcp-almacenamiento`.`dbt_analytics_analytics`.`top_5_product_expenses`
      
    
    

    
    OPTIONS()
    as (
      


with __dbt__cte__base_orders as (


SELECT
id,
customer_id,
created_at,
total_price
FROM `e2e-gcp-almacenamiento`.`orders_bronze`.`orders`
),  __dbt__cte__base_order_products as (


SELECT
order_id,
product_id,
quantity,
price
FROM `e2e-gcp-almacenamiento`.`orders_bronze`.`order_products`
),  __dbt__cte__base_products as (


SELECT
id,
product_name,
price
FROM `e2e-gcp-almacenamiento`.`orders_bronze`.`products`
) SELECT
    SUM(op.price*op.quantity) AS total_product_spent,
    product_name
    FROM
    __dbt__cte__base_orders o
    LEFT JOIN
    __dbt__cte__base_order_products op
    ON
    o.id = op.order_id
    LEFT JOIN
    __dbt__cte__base_products p
    ON
    op.product_id = p.id
    GROUP BY
    product_name
    ORDER BY
    SUM(op.price*op.quantity) DESC
    LIMIT
    5
    );
  