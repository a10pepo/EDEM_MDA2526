SELECT
    stg_race_id AS race_key,
    stg_circuit_id AS circuit_key, -- Clave del circuito (puede ser una FK a otra Dim)
    stg_race_name,
    stg_season_year,
    stg_round_number,
    CAST(stg_race_date AS DATE) AS race_date,
    CAST(stg_race_time AS TIME) AS race_time

FROM
    {{ ref('stg_races') }}

ORDER BY
    stg_season_year, stg_round_number