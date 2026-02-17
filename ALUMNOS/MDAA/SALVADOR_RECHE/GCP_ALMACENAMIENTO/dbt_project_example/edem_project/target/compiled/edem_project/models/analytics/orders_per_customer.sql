

with __dbt__cte__base_orders as (


SELECT
id,
customer_id,
created_at,
total_price
FROM `e2e-gcp-almacenamiento`.`orders_bronze`.`orders`
),  __dbt__cte__base_customers as (


SELECT
id,
customer_name,
email
FROM `e2e-gcp-almacenamiento`.`orders_bronze`.`customers`
) SELECT
    SUM(total_price) AS total_price,
    c.customer_name
    FROM
    __dbt__cte__base_orders o
    LEFT JOIN
    __dbt__cte__base_customers c
    ON
    c.id = o.customer_id
    GROUP BY
    customer_name
    ORDER BY
    total_price desc