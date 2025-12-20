with source as (
    select * from "dev"."main"."qualifying"
),

renamed as (
    select
        race_id,
        driver_id,
        constructor_id,
        cast(position as integer) as qualifying_position,
        q1 as q1_time,
        q2 as q2_time,
        q3 as q3_time
    from source
)

select * from renamed