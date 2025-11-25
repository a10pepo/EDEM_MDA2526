with base as (

    -- Partimos directamente del staging
    select * 
    from {{ ref('staging_valenbisi') }}

),

enriched as (

    select
        -- Mantener todas las columnas originales
        id,
        numero_estacion,
        nombre_estacion,
        latitud,
        longitud,
        bicicletas_disponibles,
        huecos_disponibles,
        estado_estacion,
        capacidad_total,
        momento_medicion,

        -- Nuevas métricas de disponibilidad
        bicicletas_disponibles * 1.0 / capacidad_total as porcentaje_bicis_disponibles,
        huecos_disponibles * 1.0 / capacidad_total as porcentaje_huecos_disponibles,
        capacidad_total - huecos_disponibles as ocupacion,

        -- Clasificación de situación según reglas proporcionadas
        case
            when capacidad_total = 0 then 'desconocida'  -- Evita división por cero
            when bicicletas_disponibles = capacidad_total then 'llena'
            when bicicletas_disponibles >= capacidad_total * 0.75 then 'casi llena'
            when bicicletas_disponibles >= capacidad_total * 0.50 then 'medio llena'
            when bicicletas_disponibles >= capacidad_total * 0.25 then 'medio vacía'
            when bicicletas_disponibles >= 1 then 'casi vacía'
            when bicicletas_disponibles = 0 then 'vacía'
            else 'desconocida'
        end as situacion_estacion

    from base
)

select * from enriched;
