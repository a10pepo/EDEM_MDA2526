SELECT
    -- Llaves Foráneas
    race_id AS stg_race_id,
    driver_id AS stg_driver_id,
    constructor_id AS stg_constructor_id,

    -- Métricas de Carrera
    CAST(grid AS INT) AS stg_starting_grid_position,
    
    -- Conversión de 'position' a un entero (a veces tiene 'R' o 'D', por lo que usamos 'position_order')
    CASE 
        WHEN position = '\N' THEN NULL
        ELSE CAST(position AS INT)
    END AS stg_final_position_text,
    
    CAST(position_order AS INT) AS stg_final_position_order,
    CAST(points AS DECIMAL(10, 2)) AS stg_points_awarded,
    CAST(laps AS INT) AS stg_laps_completed,
    
    -- Atributo del Resultado
    status AS stg_status

FROM
    {{ source('fuente_raw', 'results') }} 