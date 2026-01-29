with source as (

    select * from "dev"."main"."former_names"

),

renamed as (

    select
        team as nombre_actual,
        other_names as nombre_antiguo

    from source

)

select * from renamed