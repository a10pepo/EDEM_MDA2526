SELECT
    -- Llaves
    race_id AS stg_race_id,
    circuit_id AS stg_circuit_id,

    -- Atributos de la Carrera
    season AS stg_season_year,
    round AS stg_round_number,
    race_name AS stg_race_name,
    
    -- Conversiones de Fecha y Hora
    CAST(date AS DATE) AS stg_race_date,
    CAST(time AS TIME) AS stg_race_time -- Considera el tipo de dato TIME en tu DB

FROM
    {{ source('fuente_raw', 'races') }} 