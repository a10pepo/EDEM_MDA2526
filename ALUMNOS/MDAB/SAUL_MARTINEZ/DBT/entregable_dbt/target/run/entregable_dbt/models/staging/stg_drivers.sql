
  
  create view "dev"."main"."stg_drivers__dbt_tmp" as (
    with source as (
    select * from "dev"."main"."drivers"
),

renamed as (
    select
        driver_id,
        "givenName" as first_name,
        "familyName" as last_name,
        nationality as driver_nationality,
        -- Convertir texto a fecha real
        cast(dob as date) as date_of_birth
    from source
)

select * from renamed
  );
