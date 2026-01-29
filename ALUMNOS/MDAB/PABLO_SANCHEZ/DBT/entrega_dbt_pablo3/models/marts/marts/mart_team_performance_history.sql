-- Propósito: Data Mart para el análisis histórico de rendimiento (une Dimensiones y Hechos).
SELECT
    TD.Team_Key,
    BF.Matchweek_Key, 
    
    -- Dimensiones
    TD.Team_Name,
    BF.Matchweek,
    
    -- Hechos/Métricas (Fact Metrics)
    BF.Played,
    BF.Won,
    BF.Drawn,
    BF.Lost,
    BF."Goals For",
    BF."Goals Against",
    BF."Goal Difference",
    BF.Points,
    
    -- Métrica Derivada: Tasa de Victorias (%)
    CASE 
        WHEN BF.Played > 0 THEN CAST(BF.Won AS DECIMAL) / BF.Played
        ELSE 0 
    END AS Win_Rate_Pct
FROM 
    {{ ref('int_base_facts') }} AS BF -- Referencia a la tabla de hechos consolidada
INNER JOIN 
    {{ ref('int_team_dimensions') }} AS TD -- Referencia a la dimensión de equipos
    ON BF.Team = TD.Team_Name
    