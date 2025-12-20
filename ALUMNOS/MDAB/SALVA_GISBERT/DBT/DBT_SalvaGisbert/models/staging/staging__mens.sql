with

source as (

    select * from {{ source('main', 'mens') }}
),

renamed as (
    select
        "#" as contest_id,
        Year,
        {{ clean_citations('Venue') }} as place,
        {{ clean_citations('Winner') }} as gold,
        represented_country as country  
    from source
)

select * from renamed