with

source as (

    select * from read_csv_auto({{ get_raw_source('ventas') }})
),

renamed as (
    select
        id_ticket as ticket_id,
        id_cliente as cliente_id,
        id_articulo as articulo_id,
        
        -- Convertimos texto a fecha real
        try_cast(fecha as date) as fecha_venta,
        
        cantidad::int as cantidad,
        total::decimal(10,2) as importe_total

    from source
)

select * from renamed