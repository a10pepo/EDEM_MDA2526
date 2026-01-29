with source as (

    select * from {{ ref('products') }}

),

renamed as (

    select
        product_id,
        product_name,
        category,
        brand,
        price,
        rating
    from source

)

select * from renamed