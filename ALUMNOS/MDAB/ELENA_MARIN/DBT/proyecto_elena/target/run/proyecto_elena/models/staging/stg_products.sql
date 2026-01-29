
  
  create view "dev"."main"."stg_products__dbt_tmp" as (
    with source as (
    select * from "dev"."main"."products"
),

renamed as (
    select
        cast("Product ID" as integer)          as product_id,
        "Category"                             as category,
        "Sub Category"                         as sub_category,
        "Description PT"                       as description_pt,
        "Description DE"                       as description_de,
        "Description FR"                       as description_fr,
        "Description ES"                       as description_es,
        "Description EN"                       as description_en,
        "Description ZH"                       as description_zh,
        "Color"                                as color,
        "Sizes"                                as sizes,
        try_cast("Production Cost" as numeric) as production_cost
    from source
)

select * from renamed
  );
