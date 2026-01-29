with source as (

    select * from {{ source('mygoal_raw', 'status') }}

),

renamed as (
    select
        statusId                as status_id,
        name                    as status_code,
        state                   as status_category_code,
        case
            when state = 'pre' then 'Scheduled'
            when state = 'in'  then 'Live'
            when state = 'post'then 'Finished'
            else 'Unknown'
        end as status_category,
        description             as status_name

    from source
)

select * from renamed