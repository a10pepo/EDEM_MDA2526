with

source as (

    select * from read_csv_auto({{ get_raw_source('pedidos_stock') }})
),

renamed as (
    select
        id_pedido as pedido_id,
        proveedor,
        id_articulo as articulo_id,
        
        try_cast(fecha as date) as fecha_pedido,

        
        estado,
        cantidad

    from source
)

select * from renamed
