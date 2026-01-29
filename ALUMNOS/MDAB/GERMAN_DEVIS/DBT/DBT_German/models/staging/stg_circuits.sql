with source as (

    select * from {{ ref('circuits') }}

),

renamed as (

    select
        circuit_id,             -- Ya se llama bien en tu CSV
        name as circuit_name,
        locality as location,   -- En tu CSV se llama 'locality'
        country,
        lat as latitude,
        long as longitude       -- En tu CSV se llama 'long', no 'lng'
    from source

)

select * from renamed