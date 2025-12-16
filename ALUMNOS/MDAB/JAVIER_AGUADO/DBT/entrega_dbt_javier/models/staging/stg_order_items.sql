with source as (

    select * from {{ ref('order_items') }}

),

renamed as (

    select
        order_item_id,
        order_id,
        product_id,
        user_id,
        quantity,
        item_price,
        item_total
    from source

)

select * from renamed