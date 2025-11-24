with

source as (

    select * from read_csv_auto('/usr/app/practica_DBT_SALVA/data/raw__capturas.csv')
),

renamed as (
    select
        id_captura as captura_id,
        id_cliente as cliente_id,
        articulo_usado as articulo_id,
        
        especie,
        zona,
        
        try_cast(fecha as date) as fecha_captura,
        peso::decimal(10,2) as peso_kg

    from source
)

select * from renamed