with source as (

    select * from {{ ref('reviews') }}

),

renamed as (

    select
        review_id,
        order_id,
        product_id,
        user_id,
        rating,
        review_text,
        review_date
    from source

)

select * from renamed