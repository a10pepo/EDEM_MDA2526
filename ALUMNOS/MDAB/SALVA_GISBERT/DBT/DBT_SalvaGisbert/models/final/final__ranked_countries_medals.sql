with unpivoted_data as (
    -- 1. Datos de Open y Classic (Tienen Oro, Plata y Bronce)
    select open_gold_country as country from {{ ref('intermediate__classic_open') }}
    union all
    select open_silver_country from {{ ref('intermediate__classic_open') }}
    union all
    select open_bronze_country from {{ ref('intermediate__classic_open') }}
    union all
    select classic_gold_country from {{ ref('intermediate__classic_open') }}
    union all
    select classic_silver_country from {{ ref('intermediate__classic_open') }}
    union all
    select classic_bronze_country from {{ ref('intermediate__classic_open') }}

    union all

    -- 2. Datos de Mens y 212 (Solo tienen Oro/Winner en tu staging actual)
    select mens_country from {{ ref('intermediate__mens_212') }}
    union all
    select cat_212_country from {{ ref('intermediate__mens_212') }}
),

cleaned_ranking as (
    select
        country,
        count(*) as total_medals
    from unpivoted_data
    where country is not null
    group by country
)

select * from cleaned_ranking
order by total_medals desc