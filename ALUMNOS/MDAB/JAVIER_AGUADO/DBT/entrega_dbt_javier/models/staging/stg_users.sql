with source as (

    select * from {{ ref('users') }}

),

renamed as (

    select
        user_id,
        name,
        email,
        gender,
        city,
        signup_date
    from source

)

select * from renamed