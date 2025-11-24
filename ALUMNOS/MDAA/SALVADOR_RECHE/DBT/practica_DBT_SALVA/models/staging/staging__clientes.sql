with

source as (

    select * from read_csv_auto('/usr/app/practica_DBT_SALVA/data/raw__clientes.csv')),

renamed as (
    select
        id_cliente as cliente_id,
        nombre,
        municipio,
        modalidad_pref as modalidad_favorita,
        try_cast(fecha_alta as date) as fecha_alta

    from source
)

select * from renamed