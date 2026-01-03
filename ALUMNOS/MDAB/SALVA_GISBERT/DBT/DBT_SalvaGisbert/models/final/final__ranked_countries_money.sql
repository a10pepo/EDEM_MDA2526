with prizes as (
    -- Premios Open
    select 
        open_gold_country as country, 
        open_prize as prize_amount
    from {{ ref('intermediate__classic_open') }}
    
    union all

    -- Premios Classic
    select 
        classic_gold_country as country, 
        classic_prize as prize_amount
    from {{ ref('intermediate__classic_open') }}
),

aggregated_money as (
    select
        country,
        -- Sumamos y manejamos nulos por si acaso
        sum(coalesce(prize_amount, 0)) as total_prize_money
    from prizes
    where country is not null
    group by country
)

select * from aggregated_money
order by total_prize_money desc