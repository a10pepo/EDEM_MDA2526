-- models/intermediate/int_team_dimensions.sql

WITH all_teams AS (
    -- Consolidamos todos los equipos de las tablas de semillas (seeds) para asegurar la unicidad
    SELECT DISTINCT Team FROM {{ ref('premier_league_table_13') }}
    UNION DISTINCT 
    SELECT DISTINCT Team FROM {{ ref('premier_league_table_14') }}
    UNION DISTINCT 
    SELECT DISTINCT Team FROM {{ ref('premier_league_table_15') }}
)

SELECT
    -- Generamos la clave subrogada Team_Key
    ROW_NUMBER() OVER (ORDER BY Team) AS Team_Key,
    Team AS Team_Name
FROM 
    all_teams
    
