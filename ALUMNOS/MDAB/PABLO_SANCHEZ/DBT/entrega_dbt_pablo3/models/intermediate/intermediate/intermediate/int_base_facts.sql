-- models/intermediate/int_base_facts.sql

SELECT
    'PL' || Matchweek AS Matchweek_Key,
    Team,
    -- Aplicamos la conversión de tipos directamente aquí
    CAST(Played AS INT) AS Played,
    CAST(Won AS INT) AS Won,
    CAST(Drawn AS INT) AS Drawn,
    CAST(Lost AS INT) AS Lost,
    CAST("Goals For" AS INT) AS "Goals For",
    CAST("Goals Against" AS INT) AS "Goals Against",
    CAST("Goal Difference" AS INT) AS "Goal Difference",
    CAST(Points AS INT) AS Points,
    Matchweek
FROM 
    (
        -- Referenciamos los seeds (CSV) directamente
        SELECT *, 13 AS Matchweek FROM {{ ref('premier_league_table_13') }}
        UNION ALL
        SELECT *, 14 AS Matchweek FROM {{ ref('premier_league_table_14') }}
        UNION ALL
        SELECT *, 15 AS Matchweek FROM {{ ref('premier_league_table_15') }}
    ) AS All_Results_Raw
    