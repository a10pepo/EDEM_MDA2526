
  
  create view "dev"."main"."stg_races__dbt_tmp" as (
    with source as (
    select * from "dev"."main"."races"
),

renamed as (
    select
        race_id,
        cast(season as integer) as season,
        cast(round as integer) as round,
        race_name,
        circuit_id,
        cast(date as date) as race_date,
        -- A veces la hora viene nula o con formatos raros, lo dejamos como texto o intentamos time
        time as race_time, 
        circuit_id
    from source
)

select * from renamed
  );
