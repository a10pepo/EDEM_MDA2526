
  
  create view "dev"."main"."staging_former_names__dbt_tmp" as (
    with source as (

    select * from "dev"."main"."former_names"

),

renamed as (

    select
        team as nombre_actual,
        other_names as nombre_antiguo

    from source

)

select * from renamed
  );
