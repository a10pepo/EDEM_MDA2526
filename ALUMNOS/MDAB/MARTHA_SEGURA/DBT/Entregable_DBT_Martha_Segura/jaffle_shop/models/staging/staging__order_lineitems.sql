with source as (

    select * from {{ source('raw', 'items') }}

),

renamed as (
    select
        order_id              as order_id,
        id                    as lineitem_id,
        sku                   as product_id,
        price / 100           as unit_price,
        units                 as quantity,
        units * (price / 100) as subtotal_price,
        case when units > 0 then 'VENTA' else 'DEVOLUCION' end as type_of_movement
    from source
)

select * from renamed
