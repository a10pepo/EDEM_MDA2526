with raw as (
    select * from "dbt"."main"."car_sales_all"
),

clean as (
    select
        cast("Date" as date) as sale_date,
        "Salesperson" as salesperson,
        "Customer Name" as customer_name,
        "Car Make" as car_make,
        "Car Model" as car_model,
        "Car Year" as car_year,
        "Sale Price" as sale_price,
        "Commission Rate" as commission_rate,
        "Commission Earned" as commission_earned
    from raw
)

select * from clean