with source as (
    select * from {{ ref('drivers') }}
),

renamed as (
    select
        driverId as driver_id,
        driverRef as driver_ref,
        number,
        code,
        forename,
        surname,
        dob as date_of_birth,
        nationality,
        url
    from source
)

select * from renamed