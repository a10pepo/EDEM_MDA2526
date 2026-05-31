SELECT
    -- Keys
    T1.stg_race_id,
    T1.stg_driver_id,
    T1.stg_constructor_id, -- El ID del constructor se mantiene aquí

    -- Race Attributes (from stg_races R)
    R.stg_race_name,
    R.stg_race_date,
    R.stg_season_year,
    R.stg_round_number,
    
    -- Driver Attributes (from stg_drivers D)
    D.stg_given_name,
    D.stg_family_name,
    D.stg_nationality,
    
    -- Result Metrics (from stg_results T1)
    T1.stg_starting_grid_position,
    T1.stg_final_position_order,
    T1.stg_points_awarded,
    T1.stg_laps_completed,
    T1.stg_status,
    
    -- Generar una clave única para la fila (para el modelo de hechos)
    CONCAT(CAST(T1.stg_race_id AS VARCHAR), '_', T1.stg_driver_id) AS race_result_unique_key

FROM
    {{ ref('stg_results') }} T1 -- Tabla principal (Hechos)
INNER JOIN
    {{ ref('stg_races') }} R 
    ON T1.stg_race_id = R.stg_race_id
INNER JOIN
    {{ ref('stg_drivers') }} D 
    ON T1.stg_driver_id = D.stg_driver_id