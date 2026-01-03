with

classic as (
    select * from {{ ref('staging__classic') }}
),

open_cat as (
    select * from {{ ref('staging__open') }}
),

joined as (
    select
        -- 1. Llaves y datos comunes
        coalesce(open_cat.Year, classic.Year) as year,
        coalesce(open_cat.place, classic.place) as place,

        -- 2. CATEGORÍA OPEN
        open_cat.gold as open_gold,
        open_cat.gold_country as open_gold_country,
        
        open_cat.silver as open_silver,
        open_cat.silver_country as open_silver_country, -- Nuevo
        
        open_cat.bronze as open_bronze,
        open_cat.bronze_country as open_bronze_country, -- Nuevo
        
        open_cat.prize as open_prize,

        -- 3. CATEGORÍA CLASSIC
        classic.gold as classic_gold,
        classic.gold_country as classic_gold_country,
        
        classic.silver as classic_silver,
        classic.silver_country as classic_silver_country, -- Nuevo
        
        classic.bronze as classic_bronze,
        classic.bronze_country as classic_bronze_country, -- Nuevo
        
        classic.prize as classic_prize

    from open_cat
    full outer join classic 
        on open_cat.Year = classic.Year
)

select * from joined
order by year desc