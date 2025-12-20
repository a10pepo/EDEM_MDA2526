with source as (
    select * from {{ ref('circuits') }}
),

renamed as (
    select
        circuitId as circuit_id,
        circuitRef as circuit_ref,
        name,
        location,
        country,
        lat as latitude,
        lng as longitude,
        alt as altitude,
        url
    from source
)

select * from renamed