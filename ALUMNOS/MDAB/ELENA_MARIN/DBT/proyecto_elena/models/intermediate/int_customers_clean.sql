-- enriches customer data: normalizes email, splits name in two columns when possible, and calculates age (in years).

with c as (

    select * from {{ ref('stg_customers') }}

),

enriched as (

    select
        customer_id,
        customer_name,
        case
            when position(' ' in customer_name) > 0 then split_part(customer_name, ' ', 1)
            else customer_name
        end as first_name,
        case
            when position(' ' in customer_name) > 0 then
                ltrim(substr(customer_name, length(split_part(customer_name, ' ', 1)) + 1))
            else null
        end as last_name,
        email,
        telephone,
        city,
        country,
        gender,
        job_title,
        date_of_birth,
        -- estimated age in years (current year - year of birth)
        cast(strftime('%Y', current_date) as integer) - cast(strftime('%Y', date_of_birth) as integer) as age
    from c
)

select * from enriched
