SELECT
    -- Llave Primaria
    driver_id AS stg_driver_id,

    -- Atributos del Driver
    givenName AS stg_given_name,
    familyName AS stg_family_name,
    nationality AS stg_nationality,
    
    -- Conversión de Fecha de Nacimiento
    CAST(dob AS DATE) AS stg_date_of_birth

FROM
    {{ source('fuente_raw', 'drivers') }} 