with source as (

    select * from {{ source('mygoal_raw', 'keyEventDescription') }}

),

renamed as (
    select
        keyEventTypeId      as event_type_id,
        keyEventName        as event_type_name,
    
    from source
)

select * from renamed
