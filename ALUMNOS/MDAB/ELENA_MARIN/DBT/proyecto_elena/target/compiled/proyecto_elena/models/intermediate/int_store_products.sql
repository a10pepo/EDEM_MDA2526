with s as (
    select * from "dev"."main"."stg_stores"
),

p as (
    select * from "dev"."main"."int_product_financials"
),

store_products as (

    select
        s.store_id,
        s.store_name,
        s.country as store_country,
        s.city as store_city,
        p.product_id,
        p.category,
        p.sub_category,
        p.suggested_price,
        p.production_cost,
        -- ajuste local de precio según país (ejemplo simple)
        case
            when lower(s.country) = 'usa' then p.suggested_price * 1.10
            when lower(s.country) = 'spain' then p.suggested_price * 1.05
            else p.suggested_price
        end as local_price,
        current_date as price_effective_date
    from s
    cross join p
)

select * from store_products