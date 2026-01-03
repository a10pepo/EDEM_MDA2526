with

mens as (
    select * from {{ ref('staging__mens') }}
),

cat_212 as (
    select * from {{ ref('staging__212') }}
),

joined as (
    select
        -- Unificamos el año
        coalesce(mens.Year, cat_212.Year) as year,
        
        -- Lugar del evento
        coalesce(mens.place, cat_212.place) as place,
        -- Datos Men's Physique
        mens.gold as mens_gold,
        mens.country as mens_country,

        -- Datos 212 
        cat_212.gold as cat_212_gold,
        cat_212.country as cat_212_country

    from mens
    full outer join cat_212
        on mens.Year = cat_212.Year
)

select * from joined
order by year desc