with source as (
    select * from "dev"."main"."constructors"
),

renamed as (
    select
        constructor_id,
        name as constructor_name,
        nationality as constructor_nationality
    from source
)

select * from renamed