with source as (
    select * from "dev"."main"."customers"
),

renamed as (
    select
        cast("Customer ID" as integer)      as customer_id,
        "Name"                              as customer_name,
        lower("Email")                      as email,
        "Telephone"                         as telephone,
        "City"                              as city,
        "Country"                           as country,
        "Gender"                            as gender,
        try_cast("Date Of Birth" as date)   as date_of_birth,
        "Job Title"                         as job_title
    from source
)

select * from renamed