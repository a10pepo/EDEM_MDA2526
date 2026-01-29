with source as (
    select * from "dev"."main"."raw_productos"
),
renamed as (
    select
        id as producto_id,
        producto as nombre_producto,
        marca,
        categoria,
        coste_fabricacion,
        precio_venta,
        -- Calculamos aquí el margen unitario teórico
        (precio_venta - coste_fabricacion) as beneficio_unitario
    from source
)
select * from renamed