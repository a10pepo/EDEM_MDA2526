with source as (
    select * from "dev"."main"."raw_ventas"
),
renamed as (
    select
        id_ticket as venta_id,
        id_socio as socio_id,
        id_producto as producto_id,
        fecha_compra,
        cantidad,
        estado
    from source
)
select * from renamed