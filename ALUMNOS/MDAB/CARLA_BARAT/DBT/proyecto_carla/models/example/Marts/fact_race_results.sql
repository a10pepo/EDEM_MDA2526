SELECT
    -- Llave de la Fila
    race_result_unique_key,

    -- Llaves de Dimension (Foreign Keys)
    stg_race_id AS race_key,
    stg_driver_id AS driver_key,
    stg_constructor_id AS constructor_key,
    
    -- Métricas
    stg_season_year, -- Duplicar el año aquí facilita el filtrado
    stg_starting_grid_position,
    stg_final_position_order,
    stg_points_awarded,
    stg_laps_completed,
    
    -- Atributos de Status (para análisis de confiabilidad)
    stg_status

FROM
    {{ ref('int_race_results_joined') }}

ORDER BY
    stg_season_year DESC, 
    stg_round_number