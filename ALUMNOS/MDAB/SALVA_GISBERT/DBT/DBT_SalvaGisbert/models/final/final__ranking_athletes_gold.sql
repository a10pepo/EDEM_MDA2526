with winners as (
    -- Ganadores Open
    select open_gold as athlete_name, 'Open' as category from {{ ref('intermediate__classic_open') }}
    union all
    -- Ganadores Classic
    select classic_gold, 'Classic' from {{ ref('intermediate__classic_open') }}
    union all
    -- Ganadores Men's Physique
    select mens_gold, 'Mens Physique' from {{ ref('intermediate__mens_212') }}
    union all
    -- Ganadores 212
    select cat_212_gold, '212' from {{ ref('intermediate__mens_212') }}
),

ranking as (
    select
        athlete_name,
        count(*) as gold_medals,
        -- Opcional: Lista de categorías donde ganó (útil si alguien ganó en varias)
        string_agg(distinct category, ', ') as categories_won
    from winners
    where athlete_name is not null
    group by athlete_name
)

select * from ranking
order by gold_medals desc