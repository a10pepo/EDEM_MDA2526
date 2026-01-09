with

source as (

    select * from {{ source('main', '212') }}
),

renamed as (
    select
        "#" as contest_id,
        Year,
        {{ clean_citations('Venue') }} as place,
        Winner as gold ,
        represented_country as country  
    from source
)

select * from renamed