with source as (
    select * from "dev"."main"."results"
),

renamed as (
    select
        race_id,
        driver_id,
        constructor_id,
        cast(grid as integer) as grid_position,
        -- position puede contener textos como 'R', lo dejamos tal cual o usamos position_order
        position as position_text,
        cast(position_order as integer) as position_order,
        cast(points as double) as points,
        cast(laps as integer) as laps,
        status
    from source
)

select * from renamed