with

source as (

    select * from read_csv_auto({{ get_raw_source('articulos') }})
),

renamed as (
    select
        id_articulo as articulo_id,
        nombre,
        marca,
        categoria,
        subcategoria,
        gama,
        
        -- Estandarizamos el booleano
        case 
            when es_barco = 'True' then true 
            when es_barco = '1' then true
            else false 
        end as es_material_barco,
        
        precio::decimal(10,2) as precio_venta,
        coste::decimal(10,2) as coste_compra

    from source
)

select * from renamed