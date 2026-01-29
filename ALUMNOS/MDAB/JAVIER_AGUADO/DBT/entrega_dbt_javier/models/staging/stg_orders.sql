with source as (

    select * from {{ ref('orders') }}

),

renamed as (

    select
        order_id,
        user_id,
        order_date,
        order_status,
        total_amount
    from source

)

select * from renamed