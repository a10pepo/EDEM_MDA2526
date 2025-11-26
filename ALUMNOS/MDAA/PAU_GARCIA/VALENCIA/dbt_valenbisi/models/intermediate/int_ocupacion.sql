with base as (

    -- Partimos directamente del staging
    select * 
    from {{ ref('staging_valenbisi') }}

),

ocupacion as (

    select
        id,
        numero_estacion,
        nombre_estacion,
        bicicletas_disponibles,
        huecos_disponibles,
        estado_estacion,
        capacidad_total,
        momento_medicion,

        bicicletas_disponibles * 1.0 / capacidad_total as porcentaje_bicis_disponibles,
        huecos_disponibles * 1.0 / capacidad_total as porcentaje_huecos_disponibles,
        huecos_disponibles + bicicletas_disponibles as capacidad_real,
        capacidad_total - (huecos_disponibles + bicicletas_disponibles) as no_disponibles,
    

        
        case
            when capacidad_total = 0 then 'desconocida'  
            when bicicletas_disponibles * 1.0 / capacidad_total = 1 then 'llena'
            when bicicletas_disponibles * 1.0 / capacidad_total >= 0.75 then 'casi llena'
            when bicicletas_disponibles * 1.0 / capacidad_total >= 0.50 then 'medio llena'
            when bicicletas_disponibles * 1.0 / capacidad_total >= 0.25 then 'medio vacía'
            when bicicletas_disponibles * 1.0 / capacidad_total >= 0.01 then 'casi vacía'
            when bicicletas_disponibles * 1.0 / capacidad_total = 0 then 'vacía'
            else 'desconocida'
        end as situacion_ocupacion

    from base
)

select * from ocupacion
