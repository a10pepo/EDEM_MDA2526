-- Calcula un precio sugerido (markup sobre production_cost) y un campo de is_low_cost según production_cost.

with p as (

    select * from "dev"."main"."stg_products"

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
        -- precio sugerido: markup 40% sobre coste de producción (ajústalo si quieres)
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