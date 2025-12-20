with source as (
    select * from {{ ref('drivers') }}
),

renamed as (
    select
        driver_id,
        givenName as forename,       -- Renombramos para estandarizar
        familyName as surname,       -- Renombramos para estandarizar
        nationality as driver_nationality,
        dob as date_of_birth
    from source
)

select * from renamed