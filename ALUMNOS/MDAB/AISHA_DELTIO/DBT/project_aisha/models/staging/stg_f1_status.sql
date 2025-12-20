with source as (
    select * from {{ source('f1_raw', 'raw_status') }}
),

renamed as (
    select
        statusId as status_id,
        status as descripcion_estado
    from source
)

select * from renamed
