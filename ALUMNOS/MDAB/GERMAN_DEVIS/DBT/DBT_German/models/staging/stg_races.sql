with source as (

    select * from {{ ref('races') }}

),

renamed as (

    select
        race_id,
        season as year,
        round,
        circuit_id,
        race_name,        -- CAMBIO: Ya se llama así, no hace falta "name as race_name"
        date as race_date,
        time as race_time
    from source

)

select * from renamed