
  
  create view "dev"."main"."stg_circuits__dbt_tmp" as (
    with source as (
    select * from "dev"."main"."circuits"
),

renamed as (
    select
        circuit_id,
        name as circuit_name,
        cast(lat as double) as latitude,
        cast(long as double) as longitude,
        locality as city,
        country,
        "Wikipedia_url " as wikipedia_url -- ¡Fíjate en el espacio antes de cerrar las comillas!
    from source
)

select * from renamed
  );
