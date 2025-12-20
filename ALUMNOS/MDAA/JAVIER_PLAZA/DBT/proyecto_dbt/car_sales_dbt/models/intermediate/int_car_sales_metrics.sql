with base as (select * from {{ ref('stg_car_sales') }}),
metrics as (
    select
        salesperson,
        date_trunc('month', sale_date) as month,
        count(*) as total_cars_sold,
        sum(sale_price) as total_sales_amount,
        sum(commission_earned) as total_commissions
    from base
    group by 1,2
)
select * from metrics
