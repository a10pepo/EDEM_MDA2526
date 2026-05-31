with

source as (

    select * from {{ source('main', 'open') }}
),

renamed as (
    select
        a as contest_id,
        Year,
        {{ clean_money('champion_award') }} * 0.95 as prize,
        Venue as place,
        champion as gold,
        "represented_country_cham" as gold_country,
        "runner-up" as silver,
        "represented_country_runn" as silver_country,
        "3rd_place" as bronze,
        "represented_country_thir" as bronze_country        
    from source
)

select * from renamed