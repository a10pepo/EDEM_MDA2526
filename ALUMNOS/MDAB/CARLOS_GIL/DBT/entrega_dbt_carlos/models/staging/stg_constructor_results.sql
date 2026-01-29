with source as (
    select * from {{ ref('constructor_results') }}
),

renamed as (
    select
        constructorResultsId as constructor_results_id,
        raceId as race_id,
        constructorId as constructor_id,
        points,
        status
    from source
)

select * from renamed