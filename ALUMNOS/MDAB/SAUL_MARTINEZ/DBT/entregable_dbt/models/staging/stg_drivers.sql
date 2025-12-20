with source as (
    select * from {{ ref('drivers') }}
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