-- Calculates a suggested price (markup over production_cost) and an is_low_cost flag based on the production_cost.

with p as (

    select * from {{ ref('stg_products') }}

),

financials as (

    select
        product_id,
        category,
        sub_category,
        description_en,
        description_es,
        description_fr,
        description_de,
        description_pt,
        description_zh,
        color,
        sizes,
        production_cost,
        -- suggested price: markup 40% over production cost
        case
            when production_cost is null then null
            else production_cost * 1.40
        end as suggested_price,
        case
            when production_cost is null then null
            when production_cost < 5 then true
            else false
        end as is_low_cost
    from p
)

select * from financials
