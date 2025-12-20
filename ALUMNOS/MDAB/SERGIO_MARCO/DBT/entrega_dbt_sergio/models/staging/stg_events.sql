with source as (

    select * from {{ ref('events') }}

),

renamed as (

    select
        event_id,
        user_id,
        product_id,
        event_type,
        event_timestamp
    from source

)

select * from renamed