with results as (
    -- Seleccionamos explícitamente las IDs y métricas de la tabla de resultados
    select
        result_id, 
        race_id, 
        driver_id, 
        constructor_id, -- ESTA ES LA COLUMNA CRÍTICA
        grid_position, 
        finish_position, 
        position_order,
        points, 
        laps, 
        status
    from {{ ref('stg_results') }}
),

races as (
    -- Solo las columnas necesarias de la tabla de carreras
    select 
        race_id, 
        year, 
        race_name, 
        race_date 
    from {{ ref('stg_races') }}
),

drivers as (
    -- Solo las columnas necesarias de la tabla de pilotos
    select 
        driver_id, 
        forename, 
        surname, 
        driver_nationality 
    from {{ ref('stg_drivers') }}
),

constructors as (
    -- ESTA ES LA SECCIÓN QUE DEBES ENCONTRAR Y REEMPLAZAR
    select 
        constructor_id as con_id, -- APLICAMOS EL ALIAS AQUÍ
        constructor_name, 
        constructor_nationality
    from {{ ref('stg_constructors') }}
),

final as (
    select
        -- Identificadores (Claves foráneas)
        results.result_id,
        results.race_id,
        results.driver_id,
        results.constructor_id,

        -- Información de la Carrera
        races.year,
        races.race_name,
        races.race_date,
        
        -- Información del Piloto
        drivers.forename || ' ' || drivers.surname as driver_name,
        drivers.driver_nationality,

        -- Información del Constructor
        constructors.constructor_name,
        constructors.constructor_nationality,

        -- Métricas
        results.grid_position,
        results.finish_position,
        results.points,
        results.laps,
        results.status

    from results
    left join races on results.race_id = races.race_id
    left join drivers on results.driver_id = drivers.driver_id
    left join constructors on results.constructor_id = constructors.con_id -- LINEA 36
)

select * from final