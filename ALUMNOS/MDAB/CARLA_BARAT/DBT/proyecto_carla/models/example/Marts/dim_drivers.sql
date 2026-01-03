SELECT
    stg_driver_id AS driver_key,
    stg_given_name,
    stg_family_name,
    stg_nationality,
    CAST(stg_date_of_birth AS DATE) AS date_of_birth,
    
    -- Calcular la edad
    DATEDIFF('year', stg_date_of_birth, CURRENT_DATE()) AS driver_age_today

FROM
    {{ ref('stg_drivers') }}

ORDER BY
    stg_family_name, stg_given_name