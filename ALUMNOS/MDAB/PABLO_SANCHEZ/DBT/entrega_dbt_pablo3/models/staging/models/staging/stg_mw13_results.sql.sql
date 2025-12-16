SELECT
    Team,
    CAST(Played AS INT) AS Played,
    CAST(Won AS INT) AS Won,
    CAST(Drawn AS INT) AS Drawn,
    CAST(Lost AS INT) AS Lost,
    CAST("Goals For" AS INT) AS GoalsFor,
    CAST("Goals Against" AS INT) AS GoalsAgainst,
    CAST("Goal Difference" AS INT) AS GoalDifference,
    CAST(Points AS INT) AS Points,
    13 AS Matchweek -- Clave de la jornada
FROM 
    {{ ref('premier_league_table_13') }} -- Referencia al CSV original (seed)
    