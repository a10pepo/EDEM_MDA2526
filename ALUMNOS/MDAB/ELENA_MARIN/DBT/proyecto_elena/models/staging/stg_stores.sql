with source as (
    select * from {{ ref('stores') }}
),

renamed as (
    select
        cast("Store ID" as integer)           as store_id,
        "Country"                             as country,
        "City"                                as city,
        "Store Name"                          as store_name,
        try_cast("Number of Employees" as integer) as num_employees,
        "ZIP Code"                            as zip_code,
        try_cast("Latitude" as double)        as latitude,
        try_cast("Longitude" as double)       as longitude
    from source
)

select * from renamed
