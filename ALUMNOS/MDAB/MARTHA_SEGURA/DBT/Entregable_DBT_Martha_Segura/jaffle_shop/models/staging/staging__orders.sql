with source as (

    select * from {{ source('raw', 'orders') }}

),

renamed as (

    select
        id as order_id,
        store_id as location_id,
        customer as customer_id,
        cast(ordered_at as date) as order_date
    from source

)

select * from renamed
